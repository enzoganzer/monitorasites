import requests
import ssl
import socket

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from monitor import analisar_site


console = Console()


def mostrar_resultado(resultado):

    tabela = Table(
        title="Resultado do monitoramento",
        show_header=True,
        header_style="bold cyan"
    )

    tabela.add_column(
        "Informação",
        style="bold"
    )

    tabela.add_column("Resultado")

    tabela.add_row(
        "URL",
        resultado["url"]
    )

    tabela.add_row(
        "Status HTTP",
        str(resultado["status"])
    )

    tabela.add_row(
        "Classificação",
        resultado["classificacao"]
    )

    tabela.add_row(
        "Tempo de resposta",
        f'{resultado["tempo"]:.0f} ms'
    )

    if resultado["https"]:
        https = "[green]✓ HTTPS[/green]"
    else:
        https = "[red]✗ HTTP[/red]"

    tabela.add_row(
        "Protocolo",
        https
    )

    tabela.add_row(
        "Certificado SSL",
        "[green]✓ Válido[/green]"
    )

    tabela.add_row(
        "Expiração SSL",
        resultado["certificado"]
    )

    console.print()
    console.print(tabela)


def main():

    console.print(
        Panel(
            "[bold cyan]WEBSITE MONITOR[/bold cyan]",
            subtitle="Monitoramento de websites",
            border_style="cyan"
        )
    )

    url = console.input(
        "\n[bold]Digite o endereço:[/bold] "
    )

    try:

        resultado = analisar_site(url)

        mostrar_resultado(resultado)

    except requests.exceptions.Timeout:

        console.print(
            "\n[bold red]✗ O endereço demorou demais para responder.[/bold red]"
        )

    except requests.exceptions.ConnectionError:

        console.print(
            "\n[bold red]✗ Não foi possível conectar-se ao endereço.[/bold red]"
        )

    except ssl.SSLError:

        console.print(
            "\n[bold red]✗ Erro ao verificar o certificado SSL.[/bold red]"
        )

    except socket.timeout:

        console.print(
            "\n[bold red]✗ A conexão SSL demorou demais.[/bold red]"
        )

    except Exception:

        console.print(
            "\n[bold red]✗ Não foi possível analisar o endereço.[/bold red]"
        )


if __name__ == "__main__":
    main()