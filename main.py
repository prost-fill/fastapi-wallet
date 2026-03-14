from fastapi import FastAPI, HTTPException #Класс с помощью которого иницитализируем приложения
from pydantic import BaseModel, Field, field_validator

app = FastAPI() # инициализация нашего приложения

#Словарь для хранения балансов кошельков 
# Ключ - название кошелька. Значение - баланс этого кошелька

BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str = Field(... , max_length=127)
    amount: float
    description: str | None = Field(... , max_length=255)

    @field_validator('amount')
    def amount_must_be_positive(cls, value: float) -> float:
        #Проверяем что значение больше нуля
        if value < 0:
            raise ValueError("Amount must be positive")
        return value
    
    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, value:str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Wallet name cannot be empty")
        return value
    
class CreateWalletRequest(BaseModel):
    name: str = Field(... , max_length=127)
    initial_balance: float = 0

    @field_validator('name')
    def name_not_empty(cls, value:str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Wallet name cannot be empty")
        return value

    @field_validator('amount')
    def balance_bot_negative(cls, value: float) -> float:
        #Проверяем что значение больше нуля
        if value < 0:
            raise ValueError("Initial balance cannot be negative")
        return value
    
@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    '''
    Если имя кошелька не указано - считаем общий баланс \n
    Если имя указано - проверяем сущетсвует ли запрашиваемый кошелёк. Если не существует - возвращаем ошибку \n
    Если существует - возвращаем баланс конкретного кошелька \n
    '''
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code = 404,
            detail = f"Wallet '{wallet_name}' not found")
        
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}

@app.post("/wallets/{name}")
def create_wallet(wallet: CreateWalletRequest):
    '''
    Проверяем существует ли такой кошелёк\n
    Создаём новый кошелёк с начальным балансом\n
    Возвращаем информацию о созданном кошельке\n
    '''
    # Проверяем существует ли такой кошелёк
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet '{wallet.name }' already exist"
            )
    # Создаём новый кошелёк с начальным балансом
    BALANCE[wallet.name ] = wallet.initial_balance
    # Возвращаем информацию о созданном кошельке
    return {
        "message": f"Wallet '{wallet.name }' created",
        "wallet": wallet.name ,
        "balance": BALANCE[wallet.name],
    }

@app.post("/operations/income")
def add_income(operation: OperationRequest):
    '''
    Проверяем существует ли кошелёк\n
    Проверяем что сумма положительная\n
    Добавляем доход к балансу кошелька\n
    Возвращаем информацию об операции\n
    '''
    #Проверяем существует ли кошелёк
    if operation.wallet_name not in BALANCE:
        raise HTTPException(            status_code=404,
            detail=f"wallet '{operation.wallet_name}' not found"
        )


    #Добавляем доход к балансу кошелька
    BALANCE [operation.wallet_name]+= operation.amount
    #Возвращаем информацию об операции
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name],
    }
    
@app.post("/operations/expense")
def add_expense(operation: OperationRequest):
    '''
    Проверяем существует ли кошелёк\n
    Проверяем что сумма положительная\n
    Проверяем достаточно ли средств в кошельке\n
    #Вычитаем расход из баланса кошелька\n
    Возвращаем информацию об операции\n
    '''
    #Проверяем существует ли кошелёк
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"wallet '{operation.wallet_name}' not found"
        )


    #Проверяем что сумма положительная
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive",
        )
    #Проверяем достаточно ли средств на кошельке
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail = f"Insufficient funds. Available: '{BALANCE[operation.wallet_name]}'"
        )
    #Вычитаем расход из баланса кошелька
    BALANCE[operation.wallet_name]-=operation.amount
    #Возвращаем информацию об операции
    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name],
    }