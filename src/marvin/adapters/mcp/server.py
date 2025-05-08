"""MCP-Server für Marvin."""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

import websockets
from websockets.server import WebSocketServerProtocol

from marvin import __version__

# Logger einrichten
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("marvin.mcp")


class MCPServer:
    """MCP-Server für Marvin - ermöglicht kollaboratives Arbeiten an AI-Coding-Tasks."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 9000):
        """Initialisiert den MCP-Server.
        
        Args:
            host: Host-Adresse
            port: Port
        """
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.tasks: Dict[str, Dict[str, Any]] = {}
    
    async def register(self, websocket: WebSocketServerProtocol) -> None:
        """Registriert einen neuen Client.
        
        Args:
            websocket: WebSocket-Verbindung des Clients
        """
        self.clients.add(websocket)
        logger.info(f"Client registriert: {websocket.remote_address}")
        await self.notify_clients(
            {
                "type": "info",
                "message": f"Neuer Client verbunden: {websocket.remote_address}",
                "clients_count": len(self.clients),
            }
        )
    
    async def unregister(self, websocket: WebSocketServerProtocol) -> None:
        """Entfernt einen Client.
        
        Args:
            websocket: WebSocket-Verbindung des Clients
        """
        self.clients.remove(websocket)
        logger.info(f"Client getrennt: {websocket.remote_address}")
        await self.notify_clients(
            {
                "type": "info",
                "message": f"Client getrennt: {websocket.remote_address}",
                "clients_count": len(self.clients),
            }
        )
    
    async def notify_clients(self, message: Dict[str, Any]) -> None:
        """Sendet eine Nachricht an alle verbundenen Clients.
        
        Args:
            message: Die zu sendende Nachricht
        """
        if not self.clients:
            return
        
        message_json = json.dumps(message)
        await asyncio.gather(
            *[client.send(message_json) for client in self.clients]
        )
    
    async def process_message(
        self, websocket: WebSocketServerProtocol, message: Dict[str, Any]
    ) -> None:
        """Verarbeitet eine Nachricht von einem Client.
        
        Args:
            websocket: WebSocket-Verbindung des Clients
            message: Die empfangene Nachricht
        """
        message_type = message.get("type", "unknown")
        
        if message_type == "ping":
            await websocket.send(json.dumps({"type": "pong"}))
        
        elif message_type == "get_projects":
            await websocket.send(
                json.dumps(
                    {
                        "type": "projects",
                        "projects": list(self.projects.values()),
                    }
                )
            )
        
        elif message_type == "create_project":
            project_id = message.get("project_id")
            if not project_id:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "message": "Project ID is required",
                        }
                    )
                )
                return
            
            if project_id in self.projects:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "message": f"Project {project_id} already exists",
                        }
                    )
                )
                return
            
            project = {
                "id": project_id,
                "name": message.get("name", project_id),
                "description": message.get("description", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "owner": str(websocket.remote_address),
                "tasks": [],
            }
            
            self.projects[project_id] = project
            
            await self.notify_clients(
                {
                    "type": "project_created",
                    "project": project,
                }
            )
        
        elif message_type == "create_task":
            project_id = message.get("project_id")
            task_id = message.get("task_id")
            
            if not project_id or not task_id:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "message": "Project ID and Task ID are required",
                        }
                    )
                )
                return
            
            if project_id not in self.projects:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "message": f"Project {project_id} not found",
                        }
                    )
                )
                return
            
            if task_id in self.tasks:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "message": f"Task {task_id} already exists",
                        }
                    )
                )
                return
            
            task = {
                "id": task_id,
                "project_id": project_id,
                "name": message.get("name", task_id),
                "description": message.get("description", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "created",
                "owner": str(websocket.remote_address),
            }
            
            self.tasks[task_id] = task
            self.projects[project_id]["tasks"].append(task_id)
            self.projects[project_id]["updated_at"] = datetime.now().isoformat()
            
            await self.notify_clients(
                {
                    "type": "task_created",
                    "task": task,
                }
            )
        
        else:
            logger.warning(f"Unbekannter Nachrichtentyp: {message_type}")
            await websocket.send(
                json.dumps(
                    {
                        "type": "error",
                        "message": f"Unknown message type: {message_type}",
                    }
                )
            )
    
    async def handler(self, websocket: WebSocketServerProtocol) -> None:
        """Haupthandler für WebSocket-Verbindungen.
        
        Args:
            websocket: WebSocket-Verbindung des Clients
        """
        await self.register(websocket)
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.process_message(websocket, data)
                except json.JSONDecodeError:
                    logger.error(f"Ungültige JSON-Nachricht: {message}")
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Invalid JSON message",
                            }
                        )
                    )
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Verbindung geschlossen: {websocket.remote_address}")
        finally:
            await self.unregister(websocket)
    
    async def start(self) -> None:
        """Startet den MCP-Server."""
        logger.info(f"MCP-Server startet auf {self.host}:{self.port}")
        
        # Server-Info ausgeben
        logger.info(f"Marvin MCP-Server v{__version__}")
        
        # WebSocket-Server starten
        async with websockets.serve(self.handler, self.host, self.port):
            # Server läuft, bis er beendet wird
            await asyncio.Future()  # Läuft für immer


def start_server(host: str = "127.0.0.1", port: int = 9000) -> None:
    """Startet den MCP-Server.
    
    Args:
        host: Host-Adresse
        port: Port
    """
    server = MCPServer(host, port)
    asyncio.run(server.start())


if __name__ == "__main__":
    start_server()
