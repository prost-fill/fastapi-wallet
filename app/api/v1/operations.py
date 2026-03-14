from app.service import operations as operations_service
from app.schemas import OperationRequest
from fastapi import APIRouter
router = APIRouter()


@router.post("/operations/income")
def add_income(operation: OperationRequest):
    '''
    Проверяем существует ли кошелёк\n
    Проверяем что сумма положительная\n
    Добавляем доход к балансу кошелька\n
    Возвращаем информацию об операции\n
    '''
    return operations_service.add_income(operation)
    
@router.post("/operations/expense")
def add_expense(operation: OperationRequest):
    '''
    Проверяем существует ли кошелёк\n 
    Проверяем что сумма положительная\n
    Проверяем достаточно ли средств в кошельке\n
    Вычитаем расход из баланса кошелька\n
    Возвращаем информацию об операции\n
    '''
    return operations_service.add_expense(operation)
    
