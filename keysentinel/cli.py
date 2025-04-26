import typer
from typing import List
from keysentinel import (
    upsert_encrypted_fields,
    retrieve_and_decrypt_fields,
)

app = typer.Typer(help="KeySentinel CLI - Secure Token Management")

@app.command("encrypt-token")
def encrypt_token_command(
    title: str = typer.Option(..., help="Title of the item in the vault."),
    fields: List[str] = typer.Option(..., help="Fields to encrypt (only keys, values prompted securely)."),
):
    """
    Encrypt and save one or multiple fields into the vault.

    For each field, you will be prompted securely to enter the value.
    """
    field_dict = {}
    for field_key in fields:
        value = typer.prompt(f"Enter value for {field_key}", hide_input=True)
        field_dict[field_key] = value

    upsert_encrypted_fields(
        fields=field_dict,
        item_title=title,
    )
    typer.echo(f"Encrypted and saved fields under title '{title}'.")

@app.command("get-token")
def get_token_command(
    title: str = typer.Option(..., help="Title of the item in the vault."),
):
    """
    Retrieve and decrypt all fields from the vault.
    """
    fields = retrieve_and_decrypt_fields(title)
    if not fields:
        typer.echo(f"No fields found for item '{title}'.")
        raise typer.Exit(code=1)

    typer.secho(
        "\n⚠️  Sensitive credentials decrypted and displayed below.\n"
        "⚠️  Do NOT store or copy them into plaintext files or version control.\n",
        fg=typer.colors.YELLOW,
        bold=True,
    )

    for key, value in fields.items():
        typer.echo(f"{key}={value}")