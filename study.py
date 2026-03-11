from __future__ import annotations

import random
from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from terms import search_terms_data

console = Console()

CATEGORY_COLORS = {
    "Git": "cyan",
    "Python Env": "yellow",
    "AI Agents": "magenta",
    "Workflow": "blue",
}



def category_badge(category: str) -> Text:
    color = CATEGORY_COLORS.get(category, "white")
    badge = Text()
    badge.append(f" {category} ", style=f"bold black on {color}")
    return badge



def _category_markup(category: str) -> str:
    color = CATEGORY_COLORS.get(category, "white")
    return f"[bold {color}]{category}[/bold {color}]"



def _render_term_panel(term: dict, *, title: str | None = None, compact: bool = False) -> None:
    badge = _category_markup(term["category"])
    content = f"{badge}\n\n[bold]{term['definition']}[/bold]"
    if term.get("analogy"):
        content += f"\n\n[italic dim]Analogy:[/italic dim] [italic]{term['analogy']}[/italic]"
    if term.get("example") and not compact:
        content += f"\n\n[dim]Example:[/dim] [cyan]{term['example']}[/cyan]"
    console.print(Panel(content, title=title or f"[bold]{term['term']}[/bold]", border_style="white"))



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
        score_style = "bold red"
        message = "Keep studying — you'll get there."

    score_text = Text()
    score_text.append(f"{correct} / {total} correct ({pct}%)\n", style=score_style)
    score_text.append(message, style=score_style)
    console.print(Panel(score_text, title="[bold]Session Summary[/bold]", border_style="white"))

    if session["missed_terms"]:
        missed_counts = Counter(t["category"] for t in session["missed_terms"])
        focus_category, focus_count = missed_counts.most_common(1)[0]
        console.print(
            f"[dim]Most missed category:[/dim] {_category_markup(focus_category)} [dim]({focus_count} missed)[/dim]"
        )

        table = Table(title="Terms to Review", show_header=True, header_style="bold red")
        table.add_column("Term", style="bold")
        table.add_column("Category")
        table.add_column("Definition")
        seen: set[str] = set()
        for term in session["missed_terms"]:
            if term["term"] in seen:
                continue
            seen.add(term["term"])
            table.add_row(term["term"], _category_markup(term["category"]), term["definition"])
        console.print(table)



def generate_choices(correct_term: dict, all_terms: list[dict]) -> list[dict]:
    same_category = [
        term for term in all_terms if term["category"] == correct_term["category"] and term["term"] != correct_term["term"]
    ]
    others = [term for term in all_terms if term["category"] != correct_term["category"]]

    distractors: list[dict] = []
    if len(same_category) >= 2:
        distractors.extend(random.sample(same_category, 2))
    else:
        distractors.extend(same_category)

    remaining = 3 - len(distractors)
    if remaining > 0:
        pool = [term for term in others if term not in distractors]
        distractors.extend(random.sample(pool, remaining))

    return random.sample([correct_term] + distractors, 4)



def flashcard_session(terms: list[dict]) -> None:
    shuffled = terms[:]
    random.shuffle(shuffled)
    session = {"correct": 0, "incorrect": 0, "missed_terms": []}

    console.print(Rule("[bold]Flashcard Mode[/bold]"))
    console.print(f"[dim]{len(shuffled)} cards. Press Enter to flip, then mark y/n. Type q anytime after reveal to stop early.[/dim]\n")

    for index, term in enumerate(shuffled, 1):
        front = Text()
        front.append(f"Card {index}/{len(shuffled)}\n\n", style="dim")
        front.append(f"{term['term']}\n", style="bold white")
        front.append_text(category_badge(term["category"]))
        console.print(Panel(front, title="[dim]Term[/dim]", border_style="white"))

        Prompt.ask("[dim]Press Enter to reveal[/dim]", default="")
        _render_term_panel(term, title="[dim]Definition[/dim]")

        answer = Prompt.ask("Did you know it?", choices=["y", "n", "q"], default="y")
        if answer == "q":
            console.print("[dim]Ending flashcard session early.[/dim]\n")
            break
        if answer == "y":
            session["correct"] += 1
            console.print("[green]Great![/green]\n")
        else:
            session["incorrect"] += 1
            session["missed_terms"].append(term)
            console.print("[red]Noted — added to your review list.[/red]\n")

    show_session_summary(session)



def quiz_session(terms: list[dict]) -> None:
    upper_limit = min(len(terms), 15)
    question_count = int(
        Prompt.ask(
            "How many questions?",
            default=str(upper_limit),
        )
    )
    question_count = max(4, min(question_count, len(terms)))

    shuffled = random.sample(terms, question_count)
    session = {"correct": 0, "incorrect": 0, "missed_terms": []}

    console.print(Rule("[bold]Quiz Mode[/bold]"))
    console.print(f"[dim]{len(shuffled)} questions. Pick the term that matches each definition.[/dim]\n")

    for index, term in enumerate(shuffled, 1):
        choices = generate_choices(term, terms)
        correct_index = choices.index(term) + 1

        q_text = f"[bold]Q{index}/{len(shuffled)}:[/bold] {term['definition']}"
        console.print(Panel(q_text, title="[dim]Which term is this?[/dim]", border_style="white"))

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Num", style="bold cyan", width=4)
        table.add_column("Term")
        table.add_column("Category", style="dim")
        for choice_number, choice in enumerate(choices, 1):
            table.add_row(str(choice_number), f"[bold]{choice['term']}[/bold]", _category_markup(choice["category"]))
        console.print(table)

        answer = Prompt.ask("Your answer", choices=["1", "2", "3", "4", "q"], default="q")
        if answer == "q":
            console.print("[dim]Ending quiz early.[/dim]\n")
            break

        if int(answer) == correct_index:
            session["correct"] += 1
            console.print("[bold green]Correct![/bold green]\n")
        else:
            session["incorrect"] += 1
            session["missed_terms"].append(term)
            correct_text = Text()
            correct_text.append("Correct answer: ", style="red")
            correct_text.append(f"{term['term']}\n", style="bold red")
            if term.get("analogy"):
                correct_text.append(f"Analogy: {term['analogy']}\n", style="italic dim")
            if term.get("example"):
                correct_text.append(f"Example: {term['example']}", style="cyan")
            console.print(Panel(correct_text, border_style="red"))
            console.print()

    show_session_summary(session)



def browse_terms(terms: list[dict]) -> None:
    console.print(Rule("[bold]Browse Terms[/bold]"))
    page_size = 8
    sorted_terms = sorted(terms, key=lambda item: (item["category"], item["term"].lower()))

    for start in range(0, len(sorted_terms), page_size):
        chunk = sorted_terms[start : start + page_size]
        table = Table(show_header=True, header_style="bold", show_lines=True)
        table.add_column("Term", style="bold", min_width=22)
        table.add_column("Definition")
        table.add_column("Extras", width=16)

        current_category = None
        for term in chunk:
            if term["category"] != current_category:
                current_category = term["category"]
                table.add_row(
                    f"[bold]{current_category}[/bold]",
                    "",
                    "",
                    style=f"bold {CATEGORY_COLORS.get(current_category, 'white')}",
                )

            extras = []
            if term.get("analogy"):
                extras.append("Analogy")
            if term.get("example"):
                extras.append("Example")
            extras_text = ", ".join(extras) if extras else "—"
            table.add_row(term["term"], term["definition"], extras_text)

        page_number = start // page_size + 1
        total_pages = (len(sorted_terms) + page_size - 1) // page_size
        console.print(table)
        console.print(f"[dim]Page {page_number}/{total_pages}[/dim]")

        if start + page_size < len(sorted_terms):
            action = Prompt.ask("[dim]Enter to continue, q to quit[/dim]", default="")
            if action.lower() == "q":
                return



def search_terms(terms: list[dict]) -> None:
    console.print(Rule("[bold]Search Terms[/bold]"))
    console.print("[dim]Search checks term, definition, analogy, example, and category.[/dim]\n")

    while True:
        query = Prompt.ask("Search (or 'q' to quit)")
        if query.lower() == "q":
            break

        results = search_terms_data(terms, query)
        if not results:
            console.print(f"[dim]No results for '[bold]{query}[/bold]'.[/dim]\n")
            continue

        console.print(f"[dim]{len(results)} result(s) for '[bold]{query}[/bold]':[/dim]\n")
        for term in results[:8]:
            _render_term_panel(term, compact=False)

        if len(results) > 8:
            console.print(f"[dim]Showing top 8 of {len(results)} matches.[/dim]\n")


if __name__ == "__main__":
    from terms import TERMS

    browse_terms(TERMS)
