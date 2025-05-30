"""XML template value object."""

from dataclasses import dataclass
from typing import Any, Optional
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class XMLTemplate:
    """Immutable XML template value object."""
    
    content: str
    version: str = "1.0"
    encoding: str = "UTF-8"
    
    def __post_init__(self) -> None:
        """Validate the XML content."""
        try:
            ET.fromstring(self.content)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML content: {e}")
    
    def to_string(self) -> str:
        """Convert to XML string with declaration."""
        declaration = f'<?xml version="{self.version}" encoding="{self.encoding}"?>\n'
        return declaration + self.content


class XMLTemplateBuilder:
    """Builder for creating XML templates."""
    
    def __init__(self) -> None:
        self._root: Optional[ET.Element] = None
        self._current: Optional[ET.Element] = None
    
    def create_root(self, tag: str, **attrs: Any) -> 'XMLTemplateBuilder':
        """Create the root element."""
        self._root = ET.Element(tag, **attrs)
        self._current = self._root
        return self
    
    def add_element(self, tag: str, text: Optional[str] = None, **attrs: Any) -> 'XMLTemplateBuilder':
        """Add a child element to the current element."""
        if self._current is None:
            raise ValueError("No current element to add child to")
        
        element = ET.SubElement(self._current, tag, **attrs)
        if text:
            element.text = text
        return self
    
    def add_task_metadata(self, task_id: str, name: str, type: str) -> 'XMLTemplateBuilder':
        """Add task metadata section."""
        if self._current is None:
            raise ValueError("No current element")
        
        metadata = ET.SubElement(self._current, "metadata")
        ET.SubElement(metadata, "task_id").text = task_id
        ET.SubElement(metadata, "name").text = name
        ET.SubElement(metadata, "type").text = type
        return self
    
    def build(self) -> XMLTemplate:
        """Build the final XML template."""
        if self._root is None:
            raise ValueError("No root element defined")
        
        content = ET.tostring(self._root, encoding="unicode")
        return XMLTemplate(content=content)
