from fastapi import BackgroundTasks, FastAPI

app = FastAPI(title="Background Tasks")


def send_welcome_email(email: str, username: str):
    """Symulacja wysyłania e-maila (w tle)."""
    # W prawdziwej aplikacji – smtplib, SendGrid, Mailgun etc.
    import time
    time.sleep(3)  # symulacja opóźnienia
    print(f"Wysłano e-mail powitalny do {email} (użytkownik: {username})")


def log_registration(username: str):
    """Loguje rejestrację do pliku."""
    with open("registrations.log", "a") as f:
        f.write(f"Nowy użytkownik: {username}\n")


def notify_admin(username: str):
    """Wysyła powiadomienie do admina."""
    print(f"[ADMIN] Nowy użytkownik: {username}")


@app.post("/register")
async def register_user(
    username: str,
    email: str,
    background_tasks: BackgroundTasks,
):
    """Rejestruje użytkownika i wysyła e-mail w tle."""
    # ... logika rejestracji (zapis do bazy) ...

    # Dodanie zadań w tle – wykonają się PO zwróceniu odpowiedzi
    background_tasks.add_task(send_welcome_email, email, username)
    background_tasks.add_task(log_registration, username)
    background_tasks.add_task(notify_admin, username)

    return {"message": f"Użytkownik {username} zarejestrowany. E-mail zostanie wysłany."}
