import asyncio
from asyncua import Client, ua
import time


class IMM:
    def __init__(self, URL):
        self.url = URL
        self.value_True = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
        self.value_False = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
        self.client = Client(url=self.url)

    async def authenticateClient(self):
        self.client.set_user("OPCUAClient1")
        self.client.set_password("@bUmw$gn79m3^QM")

        # Connect to Client
        await self.client.connect()
        print("conncted")

    async def disconnectClient(self):
        await self.client.disconnect()

    async def IMMManualMode(self):  # Sets IMM to Manual Mode
        """
        Sets Manual Mode tag to True, sets all other modes (Auto, Semi-Auto, Stop) to False  
        """
        semiautomatic_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastHAUTO")
        await semiautomatic_tag.write_value(self.value_False)

        stop_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastSTOP")
        await stop_tag.write_value(self.value_False)

        automatic_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAUTO")
        await automatic_tag.write_value(self.value_False)

        manual_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastHAND")
        await manual_tag.write_value(self.value_True)

        await manual_tag.write_value(self.value_False)
        return

    async def unitForward(self):
        """
        Moves injection unit forward
        """
        unitBackward_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAggrZurueck")
        await unitBackward_tag.write_value(self.value_False)
        unitForward_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAggrVor")
        await unitForward_tag.write_value(self.value_True)
        time.sleep(10)
        await unitForward_tag.write_value(self.value_False)
        return

    async def unitBackward(self):
        """
        Moves injection unit forward
        """
        unitForward_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAggrVor")
        await unitForward_tag.write_value(self.value_False)

        unitBackward_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAggrZurueck")
        await unitBackward_tag.write_value(self.value_True)
        time.sleep(10)
        await unitBackward_tag.write_value(self.value_False)
        return

    async def closeMould(self):
        openMould_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastWkzOeffnen")
        await openMould_tag.write_value(self.value_False)
        closeMould_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastWkzSchliessen")
        await closeMould_tag.write_value(self.value_True)
        time.sleep(10)
        await closeMould_tag.write_value(self.value_False)
        return

    async def injectPlastic(self):
        inject_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastEinspritzen")
        await inject_tag.write_value(self.value_True)
        time.sleep(10)

        await inject_tag.write_value(self.value_False)
        return

    async def plasticize(self):
        plasticize_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastPlastifizieren")
        await plasticize_tag.write_value(self.value_True)
        time.sleep(10)
        await plasticize_tag.write_value(self.value_False)
        return

    async def openMould(self):
        closeMould_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastWkzSchliessen")
        await closeMould_tag.write_value(self.value_False)

        openMould_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastWkzOeffnen")
        await openMould_tag.write_value(self.value_True)

        time.sleep(10)

        await openMould_tag.write_value(self.value_False)
        return

    async def ejectPart(self):
        ejectorBack_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAuswZurueck")
        await ejectorBack_tag.write_value(self.value_False)

        ejectorForward_tag = self.client.get_node("ns=2;s=IMM.BOY22A.GLOBAL.dTastAuswVor")
        await ejectorForward_tag.write_value(self.value_True)
        time.sleep(3)

        await ejectorForward_tag.write_value(self.value_False)
        await ejectorBack_tag.write_value(self.value_True)

        time.sleep(3)
        await ejectorBack_tag.write_value(self.value_False)
        return

async def IMMfirstcycle(self):
    await self.authenticateClient()
    print("Client Authenticated")

    await self.IMMManualMode()
    print("IMM set to Manual Mode")

    # IMM cycle start
    await self.closeMould()
    print("Mould closed")

    await self.unitForward()
    print("Unit moved forward")

    await self.injectPlastic()
    print("Plastic injected")

    await self.plasticize()
    print("Plasticizing")

    await self.openMould()
    print("Opening mould...")


async def IMMconsequentcycle(self):
    await self.authenticateClient()
    print("Client Authenticated")
    imm_status = True

    await self.IMMManualMode()
    print("IMM set to Manual Mode")

    # IMM cycle start
    await self.closeMould()
    print("Mould closed")

    await self.injectPlastic()
    print("Plastic injected")

    await self.plasticize()
    print("Plasticizing")

    await self.openMould()
    print("Opening mould...")


async def IMMejectPart(self):
    await self.ejectPart()
    print("Part ejected")