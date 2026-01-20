"""
Єдина точка входу проєкту Promotion Hub.
Запускає scheduler, який керує всіма каналами.
"""

from core.scheduler import Scheduler


def main():
    """Запуск основного цикла Promotion Hub."""
    scheduler = Scheduler()
    scheduler.run()


if __name__ == "__main__":
    main()
