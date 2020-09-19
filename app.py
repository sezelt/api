import os
from monty.serialization import loadfn
from mp_api.core.api import MAPI

resources = {}

db_uri = os.environ.get("MPCONTRIBS_MONGO_HOST", None)

# Uncomment to use JSON store for development
# core_store = JSONStore("./test_files/materials_Li_Fe_V.json")
# task_store = JSONStore("./test_files/tasks_Li_Fe_V.json")

materials_store_json = os.environ.get("MATERIALS_STORE", "materials_store.json")
task_store_json = os.environ.get("TASK_STORE", "task_store.json")
eos_store_json = os.environ.get("EOS_STORE", "eos_store.json")
similarity_store_json = os.environ.get("SIMILARITY_STORE", "similarity_store.json")
xas_store_json = os.environ.get("XAS_STORE", "xas_store.json")

bs_store_json = os.environ.get("BS_STORE", "bs_store.json")
dos_store_json = os.environ.get("DOS_STORE", "dos_store.json")

s3_bs_index_json = os.environ.get("S3_BS_INDEX_STORE", "s3_bs_index.json")
s3_dos_index_json = os.environ.get("S3_DOS_INDEX_STORE", "s3_dos_index.json")

s3_bs_json = os.environ.get("S3_BS_STORE", "s3_bs.json")
s3_dos_json = os.environ.get("S3_DOS_STORE", "s3_dos.json")

if db_uri:
    from maggma.stores import MongoURIStore, S3Store

    materials_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="task_id",
        collection_name="materials.core",
    )

    task_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="task_id",
        collection_name="tasks",
    )

    eos_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="mp_id",
        collection_name="eos",
    )

    similarity_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="mid",
        collection_name="similarity",
    )

    xas_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="xas_id",
        collection_name="xas",
    )

    bs_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="task_id",
        collection_name="bandstructure",
    )

    s3_bs_index = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="task_id",
        collection_name="s3_bandstructure_index",
    )

    dos_store = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="task_id",
        collection_name="dos",
    )

    s3_dos_index = MongoURIStore(
        uri=f"mongodb+srv://{db_uri}",
        database="mp_core",
        key="task_id",
        collection_name="s3_dos_index",
    )

    s3_bs = S3Store(
        index=s3_bs_index,
        s3_profile="s3_role",
        bucket="mp-bandstructures",
        compress=True,
    )

    s3_dos = S3Store(
        index=s3_dos_index, s3_profile="s3_role", bucket="mp-dos", compress=True
    )


else:
    materials_store = loadfn(materials_store_json)
    task_store = loadfn(task_store_json)
    eos_store = loadfn(eos_store_json)
    similarity_store = loadfn(similarity_store_json)
    xas_store = loadfn(xas_store_json)
    bs_store = loadfn(bs_store_json)
    dos_store = loadfn(dos_store_json)
    s3_bs_index = loadfn(s3_bs_index_json)
    s3_dos_index = loadfn(s3_dos_index_json)
    s3_bs = loadfn(s3_bs_json)
    s3_dos = loadfn(s3_dos_json)

# Materials
from mp_api.materials.resources import materials_resource

resources.update({"materials": materials_resource(materials_store)})

# Tasks
from mp_api.tasks.resources import task_resource

resources.update({"tasks": task_resource(task_store)})

# Trajectory
from mp_api.tasks.resources import trajectory_resource

resources.update({"trajectory": trajectory_resource(task_store)})

# EOS
from mp_api.eos.resources import eos_resource

resources.update({"eos": eos_resource(eos_store)})

# Similarity
from mp_api.similarity.resources import similarity_resource

resources.update({"similarity": similarity_resource(similarity_store)})

# XAS
from mp_api.xas.resources import xas_resource

resources.update({"xas": xas_resource(xas_store)})

# Band Structure
from mp_api.bandstructure.resources import bs_resource

resources.update({"bs": bs_resource(bs_store, s3_bs)})

# DOS
from mp_api.dos.resources import dos_resource

resources.update({"dos": dos_resource(dos_store, s3_dos)})

api = MAPI(resources=resources)
app = api.app
