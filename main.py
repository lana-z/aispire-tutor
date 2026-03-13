import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.text import Text

from terms import TERMS, get_terms_by_category
from study import flashcard_session, quiz_session, browse_terms, search_terms

console = Console()

CATEGORIES = ["Git", "Python Env", "AI Agents", "Workflow"]


def pick_terms() -> list[dict]:
    console.print("\n[dim]Filter by category?[/dim]")
    console.print("  [bold]1[/bold] All terms")
    for i, cat in enumerate(CATEGORIES, 2):
        console.print(f"  [bold]{i}[/bold] {cat}")
    choice = Prompt.ask("Choose", choices=["1", "2", "3", "4", "5"], default="1")
    if choice == "1":
        return TERMS
    cat = CATEGORIES[int(choice) - 2]
    selected = get_terms_by_category(cat)
    console.print(f"[dim]Using {len(selected)} terms from [bold]{cat}[/bold].[/dim]\n")
    return selected


def main() -> None:
    banner = Text(justify="center")
    banner.append("aispire Vocab Tutor\n", style="bold cyan")
    banner.append(f"{len(TERMS)} terms · 4 categories · 4 study modes", style="dim")
    console.print(Panel(banner, border_style="cyan"))

    while True:
        console.print(Rule())
        console.print("[bold]Main Menu[/bold]")
        console.print("  [bold cyan]1[/bold cyan] Flashcards")
        console.print("  [bold cyan]2[/bold cyan] Quiz")
        console.print("  [bold cyan]3[/bold cyan] Browse all terms")
        console.print("  [bold cyan]4[/bold cyan] Search")
        console.print("  [bold cyan]5[/bold cyan] Quit")
        console.print("  [bold cyan]6[/bold cyan] Random Flashcard")

        choice = Prompt.ask("\nPick a mode", choices=["1", "2", "3", "4", "5","6"])

        if choice == "1":
            terms = pick_terms()
            flashcard_session(terms)
        elif choice == "2":
            terms = pick_terms()
            if len(terms) < 4:
                console.print("[red]Need at least 4 terms for quiz mode.[/red]")
            else:
                quiz_session(terms)
        elif choice == "3":
            browse_terms(TERMS)
        elif choice == "4":
            search_terms(TERMS)
        elif choice == "5":
            console.print("\n[dim]Good luck studying! Bye.[/dim]")
            break
        elif choice == "6":
            random_flashcard(TERMS)

def random_flashcard(terms: list[dict]) -> None:
    term = random.choice(terms)
    console.print(f"\n[bold]{term['term']}[/bold]")
    console.print(f"{term['definition']}")
    analogy = term.get("analogy") or "No analogy available."
    console.print(f"[dim]{analogy}[/dim]")
    example = term.get("example") or ""
    if example:
        console.print(f"[dim]Example: {example}[/dim]")
    console.print("\n[dim]Returning to main menu...[/dim]")


if __name__ == "__main__":
    main()
