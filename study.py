import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.rule import Rule
from rich.text import Text

console = Console()

CATEGORY_COLORS = {
    "Git": "cyan",
    "Python Env": "yellow",
    "AI Agents": "magenta",
    "Workflow": "blue",
}


def category_badge(category: str) -> Text:
    color = CATEGORY_COLORS.get(category, "white")
    t = Text()
    t.append(f" {category} ", style=f"bold {color} on {color}")
    return t


def _make_badge(category: str) -> str:
    color = CATEGORY_COLORS.get(category, "white")
    return f"[bold {color}][{category}][/bold {color}]"


def show_session_summary(session: dict) -> None:
    correct = session["correct"]
    incorrect = session["incorrect"]
    total = correct + incorrect
    if total == 0:
        console.print("\n[dim]No answers recorded this session.[/dim]")
        return

    pct = int(correct / total * 100)
    if pct >= 80:
        score_style = "bold green"
        message = "Excellent work!"
    elif pct >= 50:
        score_style = "bold yellow"
        message = "Good effort — keep reviewing!"
    else:
        score_style = "dim"
        message = "Keep studying — you'll get there."

    score_text = Text()
    score_text.append(f"{correct} / {total} correct ({pct}%)\n", style=score_style)
    score_text.append(message, style=score_style)
    console.print(Panel(score_text, title="[bold]Session Summary[/bold]", border_style="white"))

    if session["missed_terms"]:
        table = Table(title="Terms to Review", show_header=True, header_style="bold red")
        table.add_column("Term", style="bold")
        table.add_column("Category")
        for t in session["missed_terms"]:
            color = CATEGORY_COLORS.get(t["category"], "white")
            table.add_row(t["term"], f"[{color}]{t['category']}[/{color}]")
        console.print(table)


def generate_choices(correct_term: dict, all_terms: list[dict]) -> list[dict]:
    same_cat = [t for t in all_terms if t["category"] == correct_term["category"] and t["term"] != correct_term["term"]]
    other_cat = [t for t in all_terms if t["category"] != correct_term["category"]]
    if len(same_cat) >= 3:
        distractors = random.sample(same_cat, 3)
    else:
        distractors = same_cat + random.sample(other_cat, 3 - len(same_cat))
    return random.sample([correct_term] + distractors, 4)


def flashcard_session(terms: list[dict]) -> None:
    shuffled = terms[:]
    random.shuffle(shuffled)
    session = {"correct": 0, "incorrect": 0, "missed_terms": []}

    console.print(Rule("[bold]Flashcard Mode[/bold]"))
    console.print(f"[dim]{len(shuffled)} cards. Press Enter to flip, then mark y/n.[/dim]\n")

    for i, term in enumerate(shuffled, 1):
        badge = _make_badge(term["category"])
        front_text = f"[dim]Card {i}/{len(shuffled)}[/dim]\n\n[bold white]{term['term']}[/bold white]  {badge}"
        console.print(Panel(front_text, title="[dim]Term[/dim]", border_style="white"))

        action = Prompt.ask("[dim]Press Enter to reveal or q to quit[/dim]", default="")

        if action.lower() == "q":
            console.print("[dim]Exiting flashcards...[/dim]")
            break

        back_content = f"[bold]{term['definition']}[/bold]"
        if term["analogy"]:
            back_content += f"\n\n[dim italic]Analogy:[/dim italic] [italic]{term['analogy']}[/italic]"
        if term["example"]:
            back_content += f"\n\n[dim]Example:[/dim] [cyan]{term['example']}[/cyan]"
        console.print(Panel(back_content, title="[dim]Definition[/dim]", border_style="green"))

        answer = Prompt.ask("Did you know it? (y/n or q to quit)", choices=["y", "n", "q"], default="y")

        if answer == "q":
            console.print("[dim]Exiting flashcards...[/dim]")
            break
        if answer == "y":
            session["correct"] += 1
            console.print("[green]Great![/green]\n")
        else:
            session["incorrect"] += 1
            session["missed_terms"].append(term)
            console.print("[red]Noted — add it to your review list.[/red]\n")

    show_session_summary(session)


def quiz_session(terms: list[dict]) -> None:
    shuffled = terms[:]
    random.shuffle(shuffled)
    session = {"correct": 0, "incorrect": 0, "missed_terms": []}

    console.print(Rule("[bold]Quiz Mode[/bold]"))
    console.print(f"[dim]{len(shuffled)} questions. Pick the term that matches each definition.[/dim]\n")

    for i, term in enumerate(shuffled, 1):
        choices = generate_choices(term, terms)
        correct_index = choices.index(term) + 1

        q_text = f"[bold]Q{i}/{len(shuffled)}:[/bold] {term['definition']}"
        console.print(Panel(q_text, title="[dim]Which term is this?[/dim]", border_style="white"))

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Num", style="bold cyan", width=4)
        table.add_column("Term")
        table.add_column("Category", style="dim")
        for j, choice in enumerate(choices, 1):
            color = CATEGORY_COLORS.get(choice["category"], "white")
            table.add_row(str(j), f"[bold]{choice['term']}[/bold]", f"[{color}]{choice['category']}[/{color}]")
        console.print(table)

        answer = Prompt.ask("Your answer (1-4 or q to quit)", choices=["1", "2", "3", "4", "q"])

        if answer == "q":
            console.print("[dim]Exiting quiz...[/dim]")
            break
        if int(answer) == correct_index:
            session["correct"] += 1
            console.print("[bold green]Correct![/bold green]\n")
        else:
            session["incorrect"] += 1
            session["missed_terms"].append(term)
            correct_text = Text()
            correct_text.append(f"Correct answer: ", style="red")
            correct_text.append(f"{term['term']}\n", style="bold red")
            if term["analogy"]:
                correct_text.append(f"Analogy: {term['analogy']}", style="italic dim")
            console.print(Panel(correct_text, border_style="red"))
            console.print()

    show_session_summary(session)


def browse_terms(terms: list[dict]) -> None:
    console.print(Rule("[bold]Browse Terms[/bold]"))
    categories = list(dict.fromkeys(t["category"] for t in terms))

    PAGE_SIZE = 10
    all_rows = []
    for cat in categories:
        cat_terms = [t for t in terms if t["category"] == cat]
        all_rows.append(("header", cat, cat_terms))

    # Flatten to paginated rows
    flat: list[tuple] = []
    for _, cat, cat_terms in all_rows:
        flat.append(("sep", cat))
        for t in cat_terms:
            flat.append(("term", t))

    page_items: list = []
    page_count = 0

    def flush_page():
        nonlocal page_count
        if not page_items:
            return
        page_count += 1
        table = Table(show_header=True, header_style="bold", show_lines=True)
        table.add_column("Term", style="bold", min_width=22)
        table.add_column("Definition")
        table.add_column("Has Analogy?", justify="center", width=12)

        current_sep = None
        for item in page_items:
            if item[0] == "sep":
                current_sep = item[1]
            else:
                t = item[1]
                color = CATEGORY_COLORS.get(t["category"], "white")
                term_cell = Text()
                term_cell.append(t["term"], style="bold")
                if current_sep and page_items[0] == item:
                    pass
                cat_label = f"[{color}][{t['category']}][/{color}]"
                table.add_row(
                    f"[bold]{t['term']}[/bold]\n{cat_label}",
                    t["definition"],
                    "[green]Yes[/green]" if t["analogy"] else "[dim]—[/dim]",
                )
        console.print(table)
        page_items.clear()

    term_count = 0
    for item in flat:
        if item[0] == "sep":
            cat = item[1]
            color = CATEGORY_COLORS.get(cat, "white")
            if term_count > 0 and term_count % PAGE_SIZE == 0:
                flush_page()
                action = Prompt.ask("[dim]Enter to continue, q to quit[/dim]", default="")
                if action.lower() == "q":
                    return
            page_items.append(item)
        else:
            page_items.append(item)
            term_count += 1
            if term_count % PAGE_SIZE == 0:
                flush_page()
                action = Prompt.ask("[dim]Enter to continue, q to quit[/dim]", default="")
                if action.lower() == "q":
                    return

    flush_page()


def search_terms(terms: list[dict]) -> None:
    console.print(Rule("[bold]Search Terms[/bold]"))
    while True:
        query = Prompt.ask("Search (or 'q' to quit)")
        if query.lower() == "q":
            break
        ql = query.lower()
        results = [t for t in terms if ql in t["term"].lower() or ql in t["definition"].lower()]
        if not results:
            console.print(f"[dim]No results for '[bold]{query}[/bold]'.[/dim]\n")
        else:
            console.print(f"[dim]{len(results)} result(s) for '[bold]{query}[/bold]':[/dim]\n")
            for t in results:
                badge = _make_badge(t["category"])
                content = f"{badge}\n\n[bold]{t['definition']}[/bold]"
                if t["analogy"]:
                    content += f"\n\n[italic dim]Analogy:[/italic dim] [italic]{t['analogy']}[/italic]"
                if t["example"]:
                    content += f"\n\n[dim]Example:[/dim] [cyan]{t['example']}[/cyan]"
                console.print(Panel(content, title=f"[bold]{t['term']}[/bold]", border_style="white"))


if __name__ == "__main__":
    from terms import TERMS
    browse_terms(TERMS)
