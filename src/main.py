from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()


async def startup_cycle():

    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(config=settings)
    vectordb_provider_factory = VectorDBProviderFactory(config=settings)

    # for generation client
    app.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    # for embedding client
    app.embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_SIZE)
    
    # for vectordb client
    app.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTORDB_BACKEND
        )
    app.vectordb_client.connect()


async def shutdown_cycle():
    app.mongo_conn.close()    
    app.vectordb_client.disconnect()


app.router.lifespan.append(startup_cycle)
app.router.lifespan.append(shutdown_cycle)

app.include_router(base.base_router)
app.include_router(data.data_router)