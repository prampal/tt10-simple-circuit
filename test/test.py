import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Test all 8 cases for F = AB + C'
    for A in [0, 1]:
        for B in [0, 1]:
            for C in [0, 1]:
                dut.ui_in[0].value = A
                dut.ui_in[1].value = B
                dut.ui_in[2].value = C

                await ClockCycles(dut.clk, 1)

                expected_F = (A & B) | (1 - C)

                assert dut.uo_out[0].value == expected_F, \
                    f"F incorrect for A={A}, B={B}, C={C}"
