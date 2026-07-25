"""Basic dev toolkit example."""
from dev_toolkit_skill import DevToolkitEngine

engine = DevToolkitEngine()
engine.initialize()
r = engine.run("base64-encode", text="hello")
print(f"Encoded: {r.data.output}")
r = engine.run("uuid")
print(f"UUID:    {r.data.output}")
r = engine.run("hash", text="hello", algorithm="md5")
print(f"MD5:     {r.data.output}")