import os
import sys
from dataclasses import dataclass
from typing import Annotated, Optional

import pikepdf
import tyro
from pikepdf import Encryption, Permissions


@dataclass
class Args:
    """...in some lab somewhere, this would be extremely useful, shouldn't it?"""

    # Paths to PDF files to encrypt.
    file_paths: tyro.conf.Positional[list[str]]

    # User password for PDF encryption.
    user_password: Annotated[Optional[str], tyro.conf.arg(aliases=["-u"])] = None

    # Owner password for PDF encryption.
    owner_password: Annotated[Optional[str], tyro.conf.arg(aliases=["-o"])] = None


def error_print(msg: str):
    print(f"\033[31m\033[1mError\033[0m: {msg}", file=sys.stderr)


def success_print(msg: str):
    print(f"\033[32m\033[1mSuccess\033[0m: {msg}")


def cli(args: Args):
    if not args.file_paths:
        error_print("At least one PDF file path is required.")
        exit(1)

    try:
        if not args.user_password:
            args.user_password = input("Enter user password: ")
        assert args.user_password, "User password is required."

        if not args.owner_password:
            args.owner_password = input("Enter owner password: ")
        assert args.owner_password, "Owner password is required."

    except (KeyboardInterrupt, EOFError):
        print()
        error_print("Operation cancelled by user.")
        exit(1)

    except AssertionError as e:
        error_print(str(e))
        exit(1)

    encryption = Encryption(
        user=args.user_password,
        owner=args.owner_password,
        metadata=False,
        allow=Permissions(
            accessibility=False,
            extract=False,
            modify_annotation=False,
            modify_assembly=False,
            modify_form=False,
            modify_other=False,
            print_lowres=False,
            print_highres=True,
        ),
    )

    for file_path in args.file_paths:
        if not os.path.isfile(file_path):
            error_print(f"The file '{file_path}' does not exist.")
            continue

        new_file_path = os.path.splitext(file_path)[0] + "-pass.pdf"

        try:
            with pikepdf.open(file_path) as pdf:
                pdf.save(new_file_path, encryption=encryption)
        except pikepdf.PdfError as e:
            error_print(f"Failed to encrypt PDF: {e}")
            continue

        success_print(f"Encrypted PDF saved as '{new_file_path}'.")


def main():
    args = tyro.cli(Args)
    cli(args)


if __name__ == "__main__":
    main()
