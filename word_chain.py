"""""
Индивидуальный проект — Вариант 2: Игра в слова
Студент: Горбаненко Кирилл Дмитриевич, группа ИТ-3

Задача: по набору слов выстроить цепочку, где каждое следующее слово начинается
с той буквы, на которую заканчивается предыдущее. Слово оканчивается на «ь» —
берётся предшествующая ему буква. Последнее слово цепочки заканчивается той
же буквой, что и начинается первое слово.
"""
import sys
import os
class Node:
    def __init__(self, word: str):
        self.word = word
        self.next: "Node | None" = None
class WordList:
    def __init__(self):
        self.head: Node | None = None
        self.size: int = 0

    def append(self, word: str) -> None:
        node = Node(word)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self.size += 1

    def remove(self, word: str) -> bool:
        if self.head is None:
            return False
        if self.head.word == word:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.word == word:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False
    def to_list(self) -> list[str]:
        result = []
        current = self.head
        while current is not None:
            result.append(current.word)
            current = current.next
        return result
    def __len__(self) -> int:
        return self.size
    def __bool__(self) -> bool:
        return self.size > 0
def get_effective_last_char(word: str) -> str:
    word = word.lower()
    if len(word) >= 2 and word[-1] == "ь":
        return word[-2]
    return word[-1]
def get_first_char(word: str) -> str:
    return word.lower()[0]
def load_words_from_file(filename: str) -> WordList:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    words = content.split()
    if not words:
        raise ValueError("Файл пуст или не содержит слов.")
    wl = WordList()
    for w in words:
        wl.append(w.lower())
    return wl
def load_words_from_string(text: str) -> WordList:
    words = text.split()
    if not words:
        raise ValueError("Строка пуста.")
    wl = WordList()
    for w in words:
        wl.append(w.lower())
    return wl
def solve(remaining: WordList, chain: list[str]) -> bool:
    if not remaining:
        last_char = get_effective_last_char(chain[-1])
        first_char = get_first_char(chain[0])
        return last_char == first_char
    needed_char = get_effective_last_char(chain[-1])
    candidates = [w for w in remaining.to_list() if get_first_char(w) == needed_char]
    for candidate in candidates:
        remaining.remove(candidate)
        chain.append(candidate)
        if solve(remaining, chain):
            return True
        chain.pop()
        remaining.append(candidate)
    return False
def build_chain(word_list: WordList) -> list[str] | None:
    words = word_list.to_list()
    for start_word in words:
        remaining = WordList()
        for w in words:
            if w != start_word:
                remaining.append(w)
        chain = [start_word]
        if solve(remaining, chain):
            return chain
    return None
def save_result_to_file(filename: str, chain: list[str] | None) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        if chain is None:
            f.write("No\n")
        else:
            f.write(" ".join(chain) + "\n")
    print(f"Результат сохранён в файл: {filename}")
def print_separator() -> None:
    print("─" * 60)
def print_header() -> None:
    print_separator()
    print("  Игра в слова — поиск корректной цепочки")
    print("  Горбаненко К. Д., группа ИТ-3, вариант 2")
    print_separator()
def print_menu() -> None:
    print("\nГлавное меню:")
    print("  1. Ввести слова вручную")
    print("  2. Загрузить слова из файла")
    print("  3. Сохранить последний результат в файл")
    print("  4. Показать правила задачи")
    print("  0. Выход")
    print_separator()
def input_words_manually() -> WordList | None:
    print("\nВведите слова через пробел (строчные буквы русского алфавита):")
    line = input(">>> ").strip()
    if not line:
        print("⚠  Строка пуста. Возврат в меню.")
        return None
    for ch in line.replace(" ", ""):
        if not ("а" <= ch <= "я" or ch == "ё" or ch == "ь" or ch == "ъ"):
            print(f"⚠  Недопустимый символ «{ch}». Используйте только буквы русского алфавита.")
            return None
    try:
        return load_words_from_string(line)
    except ValueError as e:
        print(f"⚠  Ошибка: {e}")
        return None
def input_filename_for_reading() -> str | None:
    print("\nВведите путь к входному файлу:")
    path = input(">>> ").strip()
    if not path:
        print("⚠  Имя файла не может быть пустым.")
        return None
    if not os.path.exists(path):
        print(f"⚠  Файл «{path}» не найден.")
        return None
    return path
def input_filename_for_writing() -> str | None:
    print("\nВведите путь к выходному файлу:")
    path = input(">>> ").strip()
    if not path:
        print("⚠  Имя файла не может быть пустым.")
        return None
    return path
def show_rules() -> None:
    print("""
Правила задачи «Игра в слова»:
  • Дан набор слов, записанных строчными буквами русского алфавита.
  • Нужно выстроить слова в цепочку, где каждое следующее слово начинается
    с той буквы, на которую заканчивается предыдущее.
  • Если слово оканчивается на «ь», берётся предшествующая буква.
  • Последнее слово цепочки должно заканчиваться буквой, с которой начинается
    первое слово (кольцо).
  • Достаточно найти одно подходящее решение.
  • Если решение не существует — выводится «No».
""")
def run_solver(word_list: WordList) -> list[str] | None:
    words = word_list.to_list()
    print(f"\nСлова ({len(words)} шт.): {' '.join(words)}")
    print("Поиск цепочки…")
    chain = build_chain(word_list)
    print_separator()
    if chain is None:
        print("Результат: No (решение не найдено)")
    else:
        print("Результат:")
        print(" ".join(chain))
        print("\nПереходы:")
        for i, word in enumerate(chain):
            end = get_effective_last_char(word)
            if i < len(chain) - 1:
                nxt = chain[i + 1]
                print(f"  {word!s:20s} → ('{end}') → {nxt}")
            else:
                first = get_first_char(chain[0])
                ok = "✓" if end == first else "✗"
                print(f"  {word!s:20s} → ('{end}') → [{chain[0]}] {ok}")
    return chain
def main() -> None:
    print_header()
    last_chain: list[str] | None = None
    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            wl = input_words_manually()
            if wl is not None:
                last_chain = run_solver(wl)
        elif choice == "2":
            path = input_filename_for_reading()
            if path is not None:
                try:
                    wl = load_words_from_file(path)
                    last_chain = run_solver(wl)
                except (OSError, ValueError) as e:
                    print(f"⚠  Ошибка при чтении файла: {e}")
        elif choice == "3":
            if last_chain is None and last_chain != []:
                print("⚠  Нет результата для сохранения. Сначала выполните поиск.")
            else:
                path = input_filename_for_writing()
                if path is not None:
                    try:
                        save_result_to_file(path, last_chain)
                    except OSError as e:
                        print(f"⚠  Ошибка записи в файл: {e}")
        elif choice == "4":
            show_rules()
        elif choice == "0":
            print("До свидания!")
            sys.exit(0)
        else:
            print("⚠  Неверный пункт меню. Введите число от 0 до 4.")
if __name__ == "__main__":
    main()