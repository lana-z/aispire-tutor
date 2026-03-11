from __future__ import annotations

import random

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from study import browse_terms, flashcard_session, quiz_session, search_terms
from terms import CATEGORIES, TERMS, TERM_ISSUES, get_term_stats, get_terms_by_category

console = Console()



def choose_study_set() -> list[dict]:
    console.print("\n[bold]Choose your study scope[/bold]")
    console.print("  [bold]1[/bold] All terms")
    console.print("  [bold]2[/bold] Single category")
    console.print("  [bold]3[/bold] Random mini-set")

    choice = Prompt.ask("Choose", choices=["1", "2", "3"], default="1")

    if choice == "1":
        return TERMS[:]

    if choice == "2":
        for index, category in enumerate(CATEGORIES, start=1):
            console.print(f"  [bold]{index}[/bold] {category}")
        selected_index = IntPrompt.ask("Category", choices=[str(i) for i in range(1, len(CATEGORIES) + 1)])
        category = CATEGORIES[selected_index - 1]
        selected = get_terms_by_category(category)
        console.print(f"[dim]Using {len(selected)} terms from [bold]{category}[/bold].[/dim]\n")
        return selected

    max_size = min(len(TERMS), 12)
    subset_size = IntPrompt.ask("How many random terms?", default=max_size)
    subset_size = max(4, min(subset_size, len(TERMS)))
    selected = random.sample(TERMS, subset_size)
    console.print(f"[dim]Using a random set of {len(selected)} terms.[/dim]\n")
    return selected



def show_dataset_stats() -> None:
    stats = get_term_stats()
    table = Table(title="Dataset Overview", show_header=True, header_style="bold cyan")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Total terms", str(stats["total"]))
    table.add_row("With analogy", str(stats["with_analogy"]))
    table.add_row("With example", str(stats["with_example"]))
    for category, count in stats["categories"].items():
        table.add_row(f"Category: {category}", str(count))
    console.print(table)



def main() -> None:
    stats = get_term_stats()
    banner = Text(justify="center")
    banner.append("aispire Vocab Tutor\n", style="bold cyan")
    banner.append(f"{stats['total']} terms · {len(CATEGORIES)} categories · richer study flow", style="dim")
    console.print(Panel(banner, border_style="cyan"))

    if TERM_ISSUES:
        console.print("[yellow]Dataset validation warnings found:[/yellow]")
        for issue in TERM_ISSUES:
            console.print(f"  - {issue}")
        console.print()

    while True:
        console.print(Rule())
        console.print("[bold]Main Menu[/bold]")
        console.print("  [bold cyan]1[/bold cyan] Flashcards")
        console.print("  [bold cyan]2[/bold cyan] Quiz")
        console.print("  [bold cyan]3[/bold cyan] Browse all terms")
        console.print("  [bold cyan]4[/bold cyan] Search")
        console.print("  [bold cyan]5[/bold cyan] Show dataset stats")
        console.print("  [bold cyan]6[/bold cyan] Quit")

        choice = Prompt.ask("\nPick a mode", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            flashcard_session(choose_study_set())
        elif choice == "2":
            terms = choose_study_set()
            if len(terms) < 4:
                console.print("[red]Need at least 4 terms for quiz mode.[/red]")
            else:
                quiz_session(terms)
        elif choice == "3":
            browse_terms(TERMS)
        elif choice == "4":
            search_terms(TERMS)
        elif choice == "5":
            show_dataset_stats()
        elif choice == "6":
            console.print("\n[dim]Good luck studying! Bye.[/dim]")
            break


if __name__ == "__main__":
    main()
