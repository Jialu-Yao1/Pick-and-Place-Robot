import asyncio
from asyncua import Client, ua
from .imm import IMM
import time

url = "opc.tcp://192.168.9.2:49320"
namespace = ""


async def main():
    test_IMM = IMM(url)

    await test_IMM.authenticateClient()
    print("Client Authenticated")
    await test_IMM.IMMManualMode()
    print("Manual Mode")
    await test_IMM.closeMould()
    print("begin unit forward")
    await test_IMM.unitForward()

    print("Inject Plastic")
    await test_IMM.injectPlastic()
    print("Plasticize")
    await test_IMM.plasticize()
    print("Open mould")
    await test_IMM.openMould()
    print("eject part")
    await test_IMM.ejectPart()

    print("done")
    return

    # print(f"Connecting to {url}...")
    # client = Client(url = url)

    # User Authentication

    # client.set_user("OPCUAClient1")
    # client.set_password("@bUmw$gn79m3^QM")

    # Connect to Client
    # await client.connect()

    # print("Root children are", await client.nodes.root.get_children())

    # Read a tag
    # tag1 = client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dLampe")
    # tag2 = client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dAuswerfer")
    # tag3 = client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.xnBetriebsart")
    # tag4 = client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAuswVor")

    # print(f"Reading tag: {tag4} with value {await tag4.read_value()}")

    # #Write value to tag
    # dv = ua.DataValue(ua.Variant(True,ua.VariantType.Boolean))
    # #print(f"Writing to tag: {dv}")
    # await tag4.write_value(dv)

    # d3 = ua.DataValue(ua.Variant(False,ua.VariantType.Boolean))
    # #print(f"Writing to tag: {dv}")
    # await tag1.write_value(d3)

    #  #Write value to tag
    # # dv2 = ua.DataValue(ua.Variant(True,ua.VariantType.Boolean))
    # # #print(f"Writing to tag: {dv}")
    # # await tag2.write_value(dv2)

    # #Disconnect from client at the end
    # await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
