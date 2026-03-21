from celery.result import AsyncResult
from django.http import JsonResponse

from orders.tasks import send_order_confirmation


# --- Wywołanie taska z delay() ---

def create_order(request):
    # order = Order.objects.create(...)
    order_id = 1  # przykładowe ID

    # Wysyłamy task do kolejki – nie czekamy na wynik
    send_order_confirmation.delay(order_id)

    # Od razu zwracamy odpowiedź użytkownikowi
    return JsonResponse({"status": "Zamówienie przyjęte!"})


# --- Wzorzec "oddaj task ID i odpytuj" ---

def start_report(request):
    from orders.tasks import generate_report
    result = generate_report.delay(1)  # request.user.id
    return JsonResponse({"task_id": result.id})


def check_report(request, task_id):
    result = AsyncResult(task_id)
    response = {"status": result.status}

    if result.ready():
        if result.successful():
            response["result"] = result.result
        else:
            response["error"] = str(result.result)

    return JsonResponse(response)
