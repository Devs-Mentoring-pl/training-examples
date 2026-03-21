from pydantic import BaseModel, Field, field_validator, model_validator


class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)
    email: str

    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Nazwa użytkownika może zawierać tylko litery i cyfry")
        return v

    @field_validator("password")
    @classmethod
    def password_must_contain_digit(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Hasło musi zawierać przynajmniej jedną cyfrę")
        return v.strip()  # możesz też modyfikować wartość


class ChangePassword(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def passwords_must_match(self) -> "ChangePassword":
        if self.password != self.password_confirm:
            raise ValueError("Hasła muszą być identyczne")
        return self


# Przykłady użycia
user = UserRegistration(username="kacper123", password="haslo1234", email="kacper@test.pl")
print(user)

change = ChangePassword(password="nowehaslo1", password_confirm="nowehaslo1")
print(change)
