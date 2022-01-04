from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.routers import rotas_pedidos, rotas_produtos, rotas_auth
from src.jobs.write_notification import write_notification

app = FastAPI()


# CORS
origins = ['http://localhost:3000',
           'https://myapp.vercel.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


# Rotas Produtos
app.include_router(rotas_produtos.router)

# Rotas Segurança: Autenticação e Autorização
app.include_router(rotas_auth.router, prefix='/auth')

# Rotas Pedidos
app.include_router(rotas_pedidos.router)


# Background
@app.post('/send_email/{email}')
def send_email(email: str, background: BackgroundTasks):
    background.add_task(write_notification, email, 'Olá tudo bem?!')
    return {'Ok': 'Mensagem enviada'}
    

# Middleware
@app.middleware('http')
async def tempoMiddleware(request: Request, next):
    print('Interceptou Chegada...')
    
    response = await next(request)
    
    print('Interceptou Volta...')
    
    return response