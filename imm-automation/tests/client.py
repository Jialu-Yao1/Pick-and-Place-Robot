import asyncio
from asyncua import Client, ua


url = "opc.tcp://192.168.9.2:49320"
namespace = ""

async def main():
    print(f"Connecting to {url}...")
    client = Client(url = url)

    #User Authentication

    client.set_user("OPCUAClient1")
    client.set_password("@bUmw$gn79m3^QM")

    #Connect to Client
    await client.connect()

    print("Root children are", await client.nodes.root.get_children())

    # Read a tag
    tag1 = client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dLampe")
    print(f"Reading tag: {tag1} with value {await tag1.read_value()}")

    #Write value to tag
    dv = ua.DataValue(ua.Variant(False,ua.VariantType.Boolean))
    #print(f"Writing to tag: {dv}")
    await tag1.write_value(dv)

    #Disconnect from client at the end
    await client.disconnect()

if __name__=="__main__":
    asyncio.run(main())
