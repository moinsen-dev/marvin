"""
Command-line interface for Marvin.

This module provides a command-line interface for interacting with Marvin.
"""

import argparse
import os
import sys

from marvin.agents.main_agent import process_prd
from marvin.api import start_server


def parse_args(args: list[str]) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Command-line arguments

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Marvin - Convert PRDs into AI-Coding-Tasks"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process a PRD file")
    process_parser.add_argument("prd_file", help="Path to the PRD file to process")
    process_parser.add_argument(
        "--codebase", "-c", help="Path to the codebase directory (optional)"
    )
    process_parser.add_argument(
        "--output", "-o", help="Output directory for generated templates (optional)"
    )

    # Server command
    server_parser = subparsers.add_parser("server", help="Start the API server")
    server_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    server_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to (default: 8000)"
    )

    return parser.parse_args(args)


def save_results(results: list[str], output_dir: str) -> None:
    """
    Save processing results to files.

    Args:
        results: List of result strings
        output_dir: Directory to save results to
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save raw results
    with open(os.path.join(output_dir, "results.txt"), "w") as f:
        for i, result in enumerate(results):
            f.write(f"=== Result {i + 1} ===\n")
            f.write(result)
            f.write("\n\n")

    # TODO: Save structured results (templates, sequence plan) in appropriate formats

    print(f"Results saved to {output_dir}")


def main(args: list[str] | None = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code
    """
    if args is None:
        args = sys.argv[1:]

    parsed_args = parse_args(args)

    if parsed_args.command == "process":
        # Validate inputs
        if not os.path.exists(parsed_args.prd_file):
            print(f"Error: PRD file not found: {parsed_args.prd_file}")
            return 1

        if parsed_args.codebase and not os.path.isdir(parsed_args.codebase):
            print(f"Error: Codebase directory not found: {parsed_args.codebase}")
            return 1

        # Process the PRD
        print(f"Processing PRD: {parsed_args.prd_file}")
        if parsed_args.codebase:
            print(f"Using codebase: {parsed_args.codebase}")

        result = process_prd(
            parsed_args.prd_file,
            parsed_args.codebase,
            parsed_args.output
        )

        if result["status"] == "success":
            # Print results
            print("\n✅ Processing completed successfully!")
            print(f"   - Features analyzed: {result.get('features_analyzed', 0)}")
            print(f"   - Tasks generated: {result.get('tasks_generated', 0)}")
            print(f"   - Templates created: {result.get('templates_created', 0)}")
            print(f"   - Processing time: {result.get('processing_time', 0):.2f}s")
            
            if result.get('insights'):
                print("\n📊 Insights:")
                for insight in result['insights']:
                    print(f"   • {insight}")
            
            if result.get('warnings'):
                print("\n⚠️  Warnings:")
                for warning in result['warnings']:
                    print(f"   • {warning}")
            
            if result.get('output_directory'):
                print(f"\n📁 Results saved to: {result['output_directory']}")

            return 0
        else:
            print(f"❌ Error: {result.get('error_message', 'Unknown error')}")
            return 1

    elif parsed_args.command == "server":
        print(f"Starting server on {parsed_args.host}:{parsed_args.port}")
        start_server(host=parsed_args.host, port=parsed_args.port)
        return 0

    else:
        print("Error: No command specified. Use --help for available commands.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
