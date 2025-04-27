import time
import typer
from typing import List
from keysentinel import (
    upsert_encrypted_fields,
    retrieve_and_decrypt_fields,
)
from keysentinel.utils import safe_copy_to_clipboard, mask_secret_value
from keysentinel.profiles import get_token_profiles

app = typer.Typer(help="KeySentinel CLI - Secure Token Management")

# --- CLI commands ---

@app.command("encrypt-token")
def encrypt_token_command(
    title: str = typer.Option(
        ..., help="Title of the item in the vault."
    ),
    fields: List[str] = typer.Option(
        None, help="Fields to encrypt (only keys, values prompted securely)."
    ),
    profile: str = typer.Option(
        None, help="Use predefined profile (aws, github, openai etc)."
    ),
):
    """Encrypt and save one or multiple fields into the vault."""
    if not fields and not profile:
        typer.secho("❌ You must provide either --fields or --profile.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    if fields and profile:
        typer.secho("❌ Cannot use --fields and --profile together. Choose one.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    if profile:
        profile_data = profile_data = get_token_profiles().get(profile.lower())
        if not profile_data:
            typer.secho(f"❌ Profile '{profile}' not found.", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)
        fields = profile_data["fields"]

    field_dict = {}
    for field_key in fields:
        value = typer.prompt(f"Enter value for {field_key}", hide_input=True)
        field_dict[field_key] = value

    upsert_encrypted_fields(fields=field_dict, item_title=title)
    typer.echo(f"Encrypted and saved fields under title '{title}'.")

@app.command("get-token")
def get_token_command(
    title: str = typer.Option(..., help="Title of the item in the vault."),
    copy: bool = typer.Option(False, help="Copy credentials to clipboard temporarily."),
    unsafe_output: bool = typer.Option(False, help="Show real secrets instead of masked values."),
    export_env: bool = typer.Option(False, help="(Blocked) Educational only - .env export not allowed."),
    export_json: bool = typer.Option(False, help="(Blocked) Educational only - JSON export not allowed."),
    timeout: int = typer.Option(5, help="Timeout in seconds to clear credentials from memory."),
):
    """Retrieve and decrypt all fields from the vault."""

    if export_env or export_json:
        _handle_export_blocked()
        return

    fields = retrieve_and_decrypt_fields(title)
    if not fields:
        typer.echo(f"No fields found for item '{title}'.")
        raise typer.Exit(code=1)


    final_output = _generate_output_lines(fields, unsafe_output or copy)

    lines_printed = len(fields)

    if not copy:
        _print_disclaimer(unsafe_output)
        typer.echo(final_output)
        typer.secho(
            f"\n⏳ Credentials will be cleared from the screen and memory in {timeout} seconds...\n",
            fg=typer.colors.BLUE,
            bold=True,
        )

    if copy:
        try:
            safe_copy_to_clipboard(final_output, timeout=timeout)
            typer.secho(
                f"\n📋 Credentials copied to clipboard. They will be cleared in {timeout} seconds.\n",
                fg=typer.colors.GREEN,
                bold=True,
            )
            lines_printed += 2
        except RuntimeError as e:
            typer.secho(f"\n❌ {str(e)}\n", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)

    _delayed_clear_memory(timeout=timeout, lines_to_clear=lines_printed)

# --- Internal helpers ---

def _print_disclaimer(unsafe_output: bool) -> None:
    """Print security disclaimer based on output mode."""
    if unsafe_output:
        typer.secho(
            "\n⚠️  Sensitive credentials decrypted and displayed below.\n"
            "⚠️  Secrets will be cleared from memory automatically after timeout.\n"
            "⚠️  DO NOT store, copy or leak these credentials.\n",
            fg=typer.colors.RED,
            bold=True,
        )
    else:
        typer.secho(
            "\n⚠️  Sensitive credentials masked for your safety.\n"
            "⚠️  Use --unsafe-output if you really need to see them (discouraged).\n",
            fg=typer.colors.YELLOW,
            bold=True,
        )

def _handle_export_blocked() -> None:
    """Handle blocked export options (env/json)."""
    typer.secho(
        "\n⚠️  Do NOT store or copy them into plaintext files or version control.\n\n"
        "\"If it's not encrypted, it's exposed.\n"
        "If it's on disk, it's compromised.\"\n"
        "from \"The Zen of Zero Trust\"\n\n"
        "For more info:\n"
        "- run: import zero_trust\n"
        "- read: https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html\n",
        fg=typer.colors.RED,
        bold=True,
    )
    raise typer.Exit()

def _generate_output_lines(fields: dict, unsafe_output: bool) -> str:
    """Generate output text with either masked or real secrets."""
    output_lines = []
    for key, value in fields.items():
        if unsafe_output:
            output_lines.append(f"{key}={value}")
        else:
            masked_value = mask_secret_value(value)
            output_lines.append(f"{key}={masked_value}")
    return "\n".join(output_lines)

def _delayed_clear_memory(timeout: int, lines_to_clear: int) -> None:
    """Wait timeout and clear the sensitive output from terminal."""
    time.sleep(timeout)

    clear_lines = lines_to_clear + 5

    # Move cursor up and clear each line
    for _ in range(clear_lines):
        print("\033[F" + " " * 100 + "\r", end="")

    typer.secho(
        "\n✅ Secrets cleared from screen and memory after timeout.\n",
        fg=typer.colors.GREEN,
        bold=True,
    )

    time.sleep(0.5)