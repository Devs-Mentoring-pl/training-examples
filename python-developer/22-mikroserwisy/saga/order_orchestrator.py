# saga/order_orchestrator.py
from dataclasses import dataclass, field


@dataclass
class SagaStep:
    """Pojedynczy krok sagi z akcją i kompensacją."""
    name: str
    action: str          # nazwa eventu do wykonania
    compensation: str    # nazwa eventu kompensującego


@dataclass
class OrderSagaOrchestrator:
    """Orchestrator sagi zamówieniowej – zarządza krokami i kompensacjami."""
    saga_id: str
    order_id: str
    current_step: int = 0
    completed_steps: list[str] = field(default_factory=list)
    status: str = "pending"

    # Definicja kroków sagi – kolejność ma znaczenie
    steps: list[SagaStep] = field(default_factory=lambda: [
        SagaStep(
            name="payment",
            action="payment.charge",
            compensation="payment.refund",
        ),
        SagaStep(
            name="inventory",
            action="inventory.reserve",
            compensation="inventory.release",
        ),
        SagaStep(
            name="shipping",
            action="shipping.schedule",
            compensation="shipping.cancel",
        ),
    ])

    def execute_next(self) -> str | None:
        """Wykonuje następny krok sagi."""
        if self.current_step >= len(self.steps):
            self.status = "completed"
            return None

        step = self.steps[self.current_step]
        return step.action  # publikuj ten event

    def on_step_success(self) -> str | None:
        """Krok zakończony sukcesem – przejdź do następnego."""
        step = self.steps[self.current_step]
        self.completed_steps.append(step.name)
        self.current_step += 1
        return self.execute_next()

    def on_step_failure(self) -> list[str]:
        """Krok zakończony niepowodzeniem – kompensuj wszystkie poprzednie."""
        self.status = "compensating"
        compensations = []

        # Kompensujemy w odwrotnej kolejności
        for step_name in reversed(self.completed_steps):
            step = next(s for s in self.steps if s.name == step_name)
            compensations.append(step.compensation)

        self.status = "failed"
        return compensations  # publikuj te eventy


# Użycie orchestratora
saga = OrderSagaOrchestrator(saga_id="abc-123", order_id="order-456")

# Krok 1: płatność
event = saga.execute_next()      # → "payment.charge"
event = saga.on_step_success()   # → "inventory.reserve"

# Krok 2: inwentaryzacja – błąd!
compensations = saga.on_step_failure()
# → ["payment.refund"]  – cofamy tylko ukończone kroki
