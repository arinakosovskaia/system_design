import httpx

BASE_URL = "http://0.0.0.0:8000"

def test_scenario():
    res = 0
    user_data = None
    i = 0
    while res != 200:
      user_data = {
        "email": "iivanov@gmail.com" + str(i),
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "password": "qwerty1234",
        "phone": "+79999999999",
        "username": "IvanIvanov2000" + str(i)
      }
      response = httpx.post(f"{BASE_URL}/users/register", json=user_data)
      res = response.status_code
      i += 1

    # Получить токен для нового пользователя
    login_data = {
      "username": "IvanIvanov2000" + str(i - 1),
      "password": "qwerty1234"
    }
    response = httpx.post(f"{BASE_URL}/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Положить деньги на счет пользователя
    deposit_data = {"amount": 100.0}
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(f"{BASE_URL}/billing/deposit", data=deposit_data, headers=headers)
    assert response.status_code == 200

    # Сделать заказ, на который хватает денег
    order_data = {
                  "items": "string",
                  "total": 50
                 }
    response = httpx.post(f"{BASE_URL}/order/create", json=order_data, headers=headers)
    assert response.status_code == 200

    # Убедиться, что деньги сняли
    balance_response = httpx.get(f"{BASE_URL}/billing/balance", headers=headers)
    assert balance_response.status_code == 200
    assert balance_response.json()["balance"] == 50.0  # 100 - 50 = 50

    # Сделать заказ, на который не хватает денег
    order_data = {"items": "string", "total": 75.0}
    response = httpx.post(f"{BASE_URL}/order/create", json=order_data, headers=headers)
    assert response.status_code == 400

    # Проверить, что заказ сохранился как неуспешный
    previous_orders_response = httpx.get(f"{BASE_URL}/orders", headers=headers)
    assert previous_orders_response.status_code == 200
    assert len(previous_orders_response.json()) == 2  # Два заказа, один успешный, другой неуспешный

    # Проверить, что баланс не изменился
    balance_response = httpx.get(f"{BASE_URL}/billing/balance", headers=headers)
    assert balance_response.status_code == 200
    assert balance_response.json()["balance"] == 50.0

if __name__ == "__main__":
    test_scenario()

