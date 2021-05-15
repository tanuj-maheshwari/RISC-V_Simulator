0x0	0x0F40006F jal x0 244, jal x0, main
0x4	0x00100293 addi x5 x0 1, addi x5, x0, 1
0x8	0x02559C63 bne x11 x5 56, bne x11, x5, else
0xc	0x00200E93 addi x29 x0 2, addi x29, x0, 2
0x10 0x01D79333	sll x6 x15 x29, sll x6, x15, x29
0x14 0x00A303B3	add x7 x6 x10, add x7, x6, x10
0x18 0x00800E93	addi x29 x0 8, addi x29, x0, 8
0x1c 0x01D59433	sll x8 x11 x29, sll x8, x11, x29
0x20 0x008004B3	add x9 x0 x8, add x9, x0, x8
0x24 0x00400E93	addi x29 x0 4, addi x29, x0, 4
0x28 0x01D61433	sll x8 x12 x29, sll x8, x12, x29
0x2c 0x008484B3	add x9 x9 x8, add x9, x9, x8
0x30 0x00D484B3	add x9 x9 x13, add x9, x9, x13
0x34 0x0093A023	sw x9 0(x7)	sw , 9, 0(x7)
0x38 0x00178793	addi x15 x15 1, addi x15, x15, 1
0x3c 0x00008067	jalr x0 x1 0, jalr x0, x1, 0
0x40 0xFEC10113	addi x2 x2 -20, addi sp, sp, -20
0x44 0x00112823	sw x1 16(x2), sw x1, 16(sp)
0x48 0x00C12623	sw x12 12(x2), sw x12,12(sp)
0x4c 0x00D12423	sw x13 8(x2), sw x13, 8(sp)
0x50 0x00E12223	sw x14 4(x2), sw x14, 4(sp)
0x54 0x00B12023	sw x11 0(x2), sw x11, 0(sp)
0x58 0xFFF58593	addi x11 x11 -1, addi x11, x11, -1
0x5c 0x00068293	addi x5 x13 0, addi x5, x13, 0
0x60 0x00070693	addi x13 x14 0, addi x13, x14, 0
0x64 0x00028713	addi x14 x5 0, addi x14, x5, 0
0x68 0xF9DFF0EF	jal x1 -100	jal, x1, TOH
0x6c 0x00012583	lw x11 0(x2), lw x11, 0(sp)
0x70 0x00412703	lw x14 4(x2), lw x14, 4(sp)
0x74 0x00812683	lw x13 8(x2), lw x13, 8(sp)
0x78 0x00C12603	lw x12 12(x2), lw x12, 12(sp)
0x7c 0x01010113	addi x2 x2 16, addi sp, sp, 16
0x80 0x00200E93	addi x29 x0 2, addi x29, x0, 2
0x84 0x01D79333	sll x6 x15 x29, sll x6, x15, x29
0x88 0x00A303B3	add x7 x6 x10, add x7, x6, x10
0x8c 0x00800E93	addi x29 x0 8, addi x29, x0, 8
0x90 0x01D59433	sll x8 x11 x29, sll x8, x11, x29
0x94 0x008004B3	add x9 x0 x8, add x9, x0, x8
0x98 0x00400E93	addi x29 x0 4, addi x29, x0, 4
0x9c 0x01D61433	sll x8 x12 x29, sll x8, x12, x29
0xa0 0x008484B3	add x9 x9 x8, add x9, x9, x8
0xa4 0x00D484B3	add x9 x9 x13, add x9, x9, x13
0xa8 0x0093A023	sw x9 0(x7)	sw , 9, 0(x7)
0xac 0x00178793	addi x15 x15 1, addi x15, x15, 1
0xb0 0xFF010113	addi x2 x2 -16, addi sp, sp, -16
0xb4 0x00B12023	sw x11 0(x2), sw x11, 0(sp)
0xb8 0x00E12223	sw x14 4(x2), sw x14, 4(sp)
0xbc 0x00D12423	sw x13 8(x2), sw x13, 8(sp)
0xc0 0x00C12623	sw x12 12(x2), sw x12, 12(sp)
0xc4 0xFFF58593	addi x11 x11 -1, addi x11, x11, -1
0xc8 0x00060293	addi x5 x12 0, addi x5, x12, 0
0xcc 0x00070613	addi x12 x14 0, addi x12, x14, 0
0xd0 0x00028713	addi x14 x5 0, addi x14, x5, 0
0xd4 0xF31FF0EF	jal x1 -208	jal, x1, TOH
0xd8 0x01012083	lw x1 16(x2), lw x1, 16(sp)
0xdc 0x00C12603	lw x12 12(x2), lw x12,12(sp)
0xe0 0x00812683	lw x13 8(x2), lw x13, 8(sp)
0xe4 0x00412703	lw x14 4(x2), lw x14, 4(sp)
0xe8 0x00012583	lw x11 0(x2), lw x11, 0(sp)
0xec 0x01410113	addi x2 x2 20, addi sp, sp, 20
0xf0 0x00008067	jalr x0 x1 0, jalr x0, x1, 0
0xf4 0x00018513	addi x10 x3 0, addi x10, x3, 0
0xf8 0x00A00593	addi x11 x0 10, addi x11, x0, 10
0xfc 0x00A00613	addi x12 x0 10, addi x12, x0, 0xA
0x100 0x00C00693 addi x13 x0 12, addi x13, x0, 0xC
0x104 0x00B00713 addi x14 x0 11, addi x14, x0, 0xB
0x108 0xEFDFF0EF jal x1 -260, jal x1, TOH
0x10c 0x00000033 add x0 x0 x0, add x0, x0, x0
0x110 0xFFFFFFFF End Of Execution