from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest
from fastapi import APIRouter

router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    '''
    Если имя кошелька не указано - считаем общий баланс \n
    Если имя указано - проверяем сущетсвует ли запрашиваемый кошелёк. Если не существует - возвращаем ошибку \n
    Если существует - возвращаем баланс конкретного кошелька \n
    '''
    return wallets_service.get_balance(wallet_name)
    
@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    '''
    Проверяем существует ли такой кошелёк\n
    Создаём новый кошелёк с начальным балансом\n
    Возвращаем информацию о созданном кошельке\n
    '''
    return wallets_service.create_wallet(wallet)