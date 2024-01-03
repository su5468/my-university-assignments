//
//  Author: Prof. Taeweon Suh
//          Computer Science & Engineering
//          Korea University
//  Date: July 14, 2020
//  Description: Skeleton design of RV32I Single-cycle CPU
//

// need to implement : lui, addi, jal, sw, lw, xori, bgeu / jalr
// implemented : xori, bgeu / jalr

// need to implement : lui, addi, slli, add, or, lw, sw, jal, jalr

// ms6 : bltu, bge

/*

todo for ms5

<done>
1. branch calculate in EX stage
2. jump calculate in EX stage
3. add bne
4. solve control hazard

<todo>

*/


`timescale 1ns/1ns
`define simdelay 1

module rv32i_cpu (
		      input         clk, reset,
            output [31:0] pc,		  		// program counter for instruction fetch
            input  [31:0] inst, 			// incoming instruction
            output        Memwrite, 	// 'memory write' control signal
            output [31:0] Memaddr,  	// memory address 
            output [31:0] MemWdata, 	// data to write to memory
            input  [31:0] MemRdata); 	// data read from memory
 
  wire        auipc, lui;
  wire        alusrc, regwrite;
  wire [4:0]  alucontrol;
  wire        memtoreg, memwrite;
  // ######################### ms4 start
  wire [31:0] ID_inst;
  wire        memread;
  // ######################### ms4 end
  wire        branch, jal, jalr;

  //assign Memwrite = MEM_memwrite;

  // Instantiate Controller
  controller i_controller(
  // ############################ ms4 start
      .opcode		(ID_inst[6:0]), 
		.funct7		(ID_inst[31:25]), 
		.funct3		(ID_inst[14:12]), 
  // ############################ ms4 end
		.auipc		(auipc),
		.lui			(lui),
		.memtoreg	(memtoreg),
		.memwrite	(memwrite),
		.branch		(branch),
		.alusrc		(alusrc),
		.regwrite	(regwrite),
		.jal			(jal),
		.jalr			(jalr),
		.alucontrol	(alucontrol),
		// ######################### ms4 start
		.memread		(memread));
		// ######################### ms4 end

  // Instantiate Datapath
  datapath i_datapath(
		.clk				(clk),
		.reset			(reset),
		.auipc			(auipc),
		.lui				(lui),
		.memtoreg		(memtoreg),
		.memwrite		(memwrite),
		.branch			(branch),
		.alusrc			(alusrc),
		.regwrite		(regwrite),
		.jal				(jal),
		.jalr				(jalr),
		.alucontrol		(alucontrol),
		.pc				(pc),
		.inst				(inst),
		// ######################### ms4 start
		.MEM_aluout		(Memaddr), 
		// ######################### ms4 end
		.MemWdata		(MemWdata),
		.MemRdata		(MemRdata),
		// ######################### ms4 start
		.ID_inst			(ID_inst),
		.MEM_memwrite	(Memwrite),
		.memread			(memread));
		// ######################### ms4 end

endmodule


//
// Instruction Decoder 
// to generate control signals for datapath
//
module controller(input  [6:0] opcode,
                  input  [6:0] funct7,
                  input  [2:0] funct3,
                  output       auipc,
                  output       lui,
                  output       alusrc,
                  output [4:0] alucontrol,
                  output       branch,
                  output       jal,
                  output       jalr,
                  output       memtoreg,
                  output       memwrite,
                  output       regwrite,
						// ######################### ms4 start
						output		 memread);
						// ######################### ms4 end

	maindec i_maindec(
		.opcode		(opcode),
		.auipc		(auipc),
		.lui			(lui),
		.memtoreg	(memtoreg),
		.memwrite	(memwrite),
		.branch		(branch),
		.alusrc		(alusrc),
		.regwrite	(regwrite),
		.jal			(jal),
		.jalr			(jalr),
		// ######################### ms4 start
		.memread		(memread));
		// ######################### ms4 end

	aludec i_aludec( 
		.opcode     (opcode),
		.funct7     (funct7),
		.funct3     (funct3),
		.alucontrol (alucontrol));


endmodule


//
// RV32I Opcode map = Inst[6:0]
//
`define OP_R			7'b0110011
`define OP_I_ARITH	7'b0010011
`define OP_I_LOAD  	7'b0000011
`define OP_I_JALR  	7'b1100111
`define OP_S			7'b0100011
`define OP_B			7'b1100011
`define OP_U_LUI		7'b0110111
`define OP_J_JAL		7'b1101111
// #################### start
`define OP_J_JALR    7'b1100111
// #################### end

//
// Main decoder generates all control signals except alucontrol 
//
//
module maindec(input  [6:0] opcode,
               output       auipc,
               output       lui,
               output       regwrite,
               output       alusrc,
               output       memtoreg, memwrite,
               output       branch, 
               output       jal,
               output       jalr,
					// ######################### ms4 start
					output       memread);
					// ######################### ms4 end

// ######################### ms4 start
  reg [9:0] controls;

  assign {auipc, lui, regwrite, alusrc, 
			 memtoreg, memwrite, branch, jal, 
			 jalr, memread} = controls;

  always @(*)
  begin
    case(opcode)
      `OP_R: 			controls <= #`simdelay 10'b0010_0000_00; // R-type
      `OP_I_ARITH: 	controls <= #`simdelay 10'b0011_0000_00; // I-type Arithmetic
      `OP_I_LOAD: 	controls <= #`simdelay 10'b0011_1000_01; // I-type Load
      `OP_S: 			controls <= #`simdelay 10'b0001_0100_00; // S-type Store
      `OP_B: 			controls <= #`simdelay 10'b0000_0010_00; // B-type Branch
      `OP_U_LUI: 		controls <= #`simdelay 10'b0111_0000_00; // LUI
      `OP_J_JAL: 		controls <= #`simdelay 10'b0011_0001_00; // JAL
	  // #################### start
		`OP_J_JALR:    controls <= #`simdelay 10'b0011_0000_10; // JALR
	  // #################### end
      default:    	controls <= #`simdelay 10'b0000_0000_00; // ???
    endcase
  end
// ######################### ms4 start
  
endmodule


//
// ALU decoder generates ALU control signal (alucontrol)
//
module aludec(input      [6:0] opcode,
              input      [6:0] funct7,
              input      [2:0] funct3,
              output reg [4:0] alucontrol);

  always @(*)

    case(opcode)

      `OP_R:   		// R-type
		begin
			case({funct7,funct3})
			 10'b0000000_000: alucontrol <= #`simdelay 5'b00000; // addition (add)
			 10'b0100000_000: alucontrol <= #`simdelay 5'b10000; // subtraction (sub)
			 10'b0000000_111: alucontrol <= #`simdelay 5'b00001; // and (and)
			 10'b0000000_110: alucontrol <= #`simdelay 5'b00010; // or (or)
          default:         alucontrol <= #`simdelay 5'bxxxxx; // ???
        endcase
		end

      `OP_I_ARITH:   // I-type Arithmetic
		begin
			case(funct3)
			 3'b000:  alucontrol <= #`simdelay 5'b00000; // addition (addi)
			 3'b110:  alucontrol <= #`simdelay 5'b00010; // or (ori)
			 3'b111:  alucontrol <= #`simdelay 5'b00001; // and (andi)
			 // ################ start
			 3'b100:  alucontrol <= #`simdelay 5'b00011; // xor (xori)
			 // ################ end
			 // ################ ms4 start
			 3'b001:  alucontrol <= #`simdelay 5'b00100; // sll (slli)
			 // ################ ms4 end
          default: alucontrol <= #`simdelay 5'bxxxxx; // ???
        endcase
		end

      `OP_I_LOAD: 	// I-type Load (LW, LH, LB...)
      	alucontrol <= #`simdelay 5'b00000;  // addition 

      `OP_B:   		// B-type Branch (BEQ, BNE, ...)
      	alucontrol <= #`simdelay 5'b10000;  // subtraction 

      `OP_S:   		// S-type Store (SW, SH, SB)
      	alucontrol <= #`simdelay 5'b00000;  // addition 

      `OP_U_LUI: 		// U-type (LUI)
      	alucontrol <= #`simdelay 5'b00000;  // addition
	  // #################### start
		`OP_J_JALR:    // JALR
			alucontrol <= #`simdelay 5'b00000;  // addition
	  // #################### end
      default: 
      	alucontrol <= #`simdelay 5'b00000;  // 

    endcase
    
endmodule


//
// CPU datapath
//
module datapath(input         clk, reset,
                input  [31:0] inst,
                input         auipc,
                input         lui,
                input         regwrite,
                input         memtoreg,
                input         memwrite,
                input         alusrc, 
                input  [4:0]  alucontrol,
                input         branch,
                input         jal,
                input         jalr,

                output reg [31:0] pc,
                output reg [31:0] MEM_aluout,
                output [31:0] MemWdata,
                input  [31:0] MemRdata,
					 // ######################### ms4 start
					 output reg		MEM_memwrite,
					 output reg [31:0] ID_inst,
					 input         memread);
					 // ######################### ms4 end

  wire [4:0]  rs1, rs2, rd;
  wire [2:0]  funct3;
  wire [31:0] rs1_data, rs2_data;
  reg  [31:0] rd_data;
  wire [20:1] jal_imm;
  wire [31:0] se_jal_imm;
  // #################### start
//  wire [12:1] jalr_imm;
//  wire [31:0] se_jalr_imm;
  // #################### end
  wire [12:1] br_imm;
  wire [31:0] se_br_imm;
  wire [31:0] se_imm_itype;
  wire [31:0] se_imm_stype;
  wire [31:0] auipc_lui_imm;
  reg  [31:0] alusrc1;
  reg  [31:0] alusrc2;
  // #################### start
  wire [31:0] branch_dest, jal_dest, jalr_dest;
  // #################### end
  wire		  Nflag, Zflag, Cflag, Vflag;
  // ############################ ms5 start
  // ############################ ms6 start
  wire		  f3beq, f3blt, f3bgeu, f3bne, f3bltu, f3bge;
  // ############################ ms6 end
  // ############################ ms5 end
  wire		  beq_taken;
  wire		  blt_taken;
  // #################### start
  wire        bgeu_taken;
  // #################### end
  // #################### ms5 start
  wire        bne_taken;
  // #################### ms5 end
  // ############################ ms6 start
  wire	     bltu_taken;
  wire        bge_taken;
  
  // #################### ms4 start
  
  wire [31:0] aluout;
  
  //reg [31:0] ID_inst;
  reg [31:0] ID_pc;
  
  reg [31:0] EX_pc;
  reg [31:0] EX_inst;
  reg EX_memtoreg;
  reg EX_memwrite;
  reg EX_branch;
  reg EX_alusrc;
  reg EX_regwrite;
  reg EX_jal;
  reg EX_jalr;
  reg [4:0] EX_alucontrol;
  reg [31:0] EX_alusrc1;
  reg [31:0] EX_alusrc2;
  reg [31:0] EX_rs2_data;
  reg [4:0] EX_rd;
  reg [31:0] EX_se_jal_imm;
  reg [31:0] EX_se_br_imm;
  reg [2:0] EX_funct3;
  reg EX_memread;
  /*
  reg [4:0] EX_rs1;
  reg [4:0] EX_rs2;
  reg [31:0] EX_rs1_data;
  reg [31:0] EX_auipc_lui_imm;
  reg [31:0] EX_se_imm_itype;
  reg [31:0] EX_se_imm_stype;
  reg EX_auipc;
  reg EX_lui;
  */
  reg [31:0] MEM_rs2_data;
  //reg [31:0] MEM_aluout;
  reg [31:0] MEM_pc;
  reg MEM_memtoreg;
  reg MEM_regwrite;
  reg MEM_jal;
  reg MEM_jalr;
  reg [4:0] MEM_rd;
  // reg MEM_memwrite;
  reg [31:0] MEM_jal_dest;
  reg [31:0] MEM_branch_dest;
  reg [31:0] MEM_jalr_dest;
  reg MEM_beq_taken;
  reg MEM_blt_taken;
  reg MEM_bgeu_taken;
  reg MEM_memread;
  // ############################ ms5 start
  reg MEM_bne_taken;
  // ############################ ms5 end
  // ############################ ms6 start
  reg MEM_bltu_taken;
  reg MEM_bge_taken;
  // ############################ ms6 end
  
  
  reg [31:0] WB_aluout;
  reg [4:0] WB_rd;
  reg [31:0] WB_pc;
  reg [31:0] WB_MemRdata;
  reg WB_regwrite;
  reg WB_memtoreg;
  reg WB_jal;
  reg WB_jalr;
  
  reg [31:0] rs1_forward;
  reg [31:0] rs2_forward;
  
  reg enable;
  reg bubble;
  
  // #################### ms4 end
  
  
  // ############################ ms4 start
  
  assign rs1 = ID_inst[19:15];
  assign rs2 = ID_inst[24:20];
  assign rd  = ID_inst[11:7];
  assign funct3  = ID_inst[14:12];
  
  // ############################ ms4 end

  //
  // PC (Program Counter) logic 
  //
  // ############################ ms4 start
  assign f3beq  = (EX_funct3 == 3'b000);
  assign f3blt  = (EX_funct3 == 3'b100);
  // #################### start
  assign f3bgeu = (EX_funct3 == 3'b111);
  // #################### end
  // ############################ ms5 start
  assign f3bne  = (EX_funct3 == 3'b001);
  // ############################ ms5 end
  // ############################ ms6 start
  assign f3bltu = (EX_funct3 == 3'b110);
  assign f3bge  = (EX_funct3 == 3'b101);
  // ############################ ms6 end

  assign beq_taken  =  EX_branch & f3beq & Zflag;
  assign blt_taken  =  EX_branch & f3blt & (Nflag != Vflag);
  // #################### start
  assign bgeu_taken =  EX_branch & f3bgeu & Cflag;
  // #################### end
  // ############################ ms5 start
  assign bne_taken  =  EX_branch & f3bne & ~Zflag;
  // ############################ ms5 end
  // ############################ ms6 start
  assign bltu_taken =  EX_branch & f3bltu & ~Cflag;
  assign bge_taken  =  EX_branch & f3bge  & Nflag == Vflag;
  // ############################ ms6 end

  // ############################ ms4 end
  
  assign branch_dest = (EX_pc + EX_se_br_imm);
  assign jal_dest 	= (EX_pc + EX_se_jal_imm);
  // #################### start
  assign jalr_dest   = {aluout[31:1],1'b0};
  // #################### end
  
  // ########################### ms4 start

	  always @(posedge clk, posedge reset)
  begin
     if (reset)  pc <= 32'b0;
	  else if (enable)
	  begin
	  // #################### start
	  // ############################ ms5 start
	  // ############################ ms6 start
			if (beq_taken | blt_taken | bgeu_taken | bne_taken | bltu_taken | bge_taken) // branch_taken
			// ############################ ms6 end
			// ############################ ms5 end
	  // #################### end
				pc <= #`simdelay branch_dest;
		   else if (EX_jal) // jal
				pc <= #`simdelay jal_dest;
	  // #################### start
			else if (EX_jalr) // jalr
			   pc <= #`simdelay jalr_dest;
	  // #################### start
		   else
			pc <= #`simdelay (pc + 4);
		end
		else
			pc <= pc;
	
  end
  // JAL immediate
  assign jal_imm[20:1] = {ID_inst[31],ID_inst[19:12],ID_inst[20],ID_inst[30:21]};
  assign se_jal_imm[31:0] = {{11{jal_imm[20]}},jal_imm[20:1],1'b0};

  // Branch immediate
  assign br_imm[12:1] = {ID_inst[31],ID_inst[7],ID_inst[30:25],ID_inst[11:8]};
  assign se_br_imm[31:0] = {{19{br_imm[12]}},br_imm[12:1],1'b0};

  // ######################### ms4 start ID
  
  always @(posedge clk)
  begin
  if(bubble)
	begin
	ID_pc <= pc;
	ID_inst <= 32'b000000000000_00000_000_00000_0010011; // addi x0, x0, 0
	end
  else if(enable)
	begin
	ID_pc <= pc;
	ID_inst <= inst;
	end
  else
	begin
	ID_inst <= ID_inst;
	ID_pc <= ID_pc;
	end
  end
  
  // ######################### ms4 end
  
  // ######################### ms4 start EX
  
  always @(posedge clk)
  begin
  // ######################### ms5 start
  if(enable && ~bubble)
  // ######################### ms5 end
	begin
	EX_pc <= ID_pc;
	EX_inst <= ID_inst;   					// don't need?
  // control signals
	//EX_auipc <= auipc;               // don't need?
	//EX_lui <= lui;                   // don't need?
	EX_memtoreg <= memtoreg;
	EX_memwrite <= memwrite;
	EX_branch <= branch;
	EX_alusrc <= alusrc;
	EX_regwrite <= regwrite;
	EX_jal <= jal;
	EX_jalr <= jalr;
	EX_alucontrol <= alucontrol;
	// others
	EX_alusrc1 <= alusrc1;      		// don't need?
	EX_alusrc2 <= alusrc2;				// don't need?
	EX_rs2_data <= rs2_forward;        // is it right?
	EX_rd <= rd;
	EX_memread <= memread;
	// pc update
	EX_se_jal_imm <= se_jal_imm;
	EX_se_br_imm <= se_br_imm;
	EX_funct3 <= funct3;
	/*
	EX_rs1 <= rs1;
	EX_rs2 <= rs2;
	EX_rs1_data <= rs1_forward;
	EX_auipc_lui_imm <= auipc_lui_imm;
	EX_se_imm_itype <= se_imm_itype;
	EX_se_imm_stype <= se_imm_stype;
	*/
	end
  else
	begin
	EX_memtoreg <= 1'b0;
	EX_memwrite <= 1'b0;
	//EX_auipc <= 1'b0;               // don't need?
	//EX_lui <= 1'b0;  	              // don't need?
	EX_branch <= 1'b0;
	EX_alusrc <= 1'b0;
	EX_regwrite <= 1'b0;
	EX_jal <= 1'b0;
	EX_jalr <= 1'b0;
	EX_alucontrol <= 5'b0;
	EX_alusrc1 <= 32'b0;				// don't need?
	EX_alusrc2 <= 32'b0;  			// don't need?
	EX_rs2_data <= 32'b0;
	EX_rd <= 5'b0;
	EX_memread <= 1'b0;
	/*
	EX_rs1 <= 5'b0;
	EX_rs2 <= 5'b0;
	EX_rs1_data <= 32'b0;
	*/
	end
  end
  
  // ######################### ms4 end
  
  // ######################### ms4 start MEM
  
  always @(posedge clk)
  begin
	MEM_rs2_data <= EX_rs2_data;
	MEM_aluout <= aluout;
	MEM_pc <= EX_pc;
	MEM_memtoreg <= EX_memtoreg;
	MEM_regwrite <= EX_regwrite;
	MEM_jal <= EX_jal;
	MEM_jalr <= EX_jalr;
	MEM_rd <= EX_rd;
	MEM_memwrite <= EX_memwrite;
	MEM_memread <= EX_memread;
	// pc update
	MEM_jal_dest <= jal_dest;
	MEM_branch_dest <= branch_dest;
	MEM_jalr_dest <= jalr_dest;
	MEM_beq_taken <= beq_taken;
	MEM_blt_taken <= blt_taken;
	MEM_bgeu_taken <= bgeu_taken;
	// ############################ ms5 start
	MEM_bne_taken <= bne_taken;
	// ############################ ms5 end
	// ############################ ms6 start
	MEM_bltu_taken <= bltu_taken;
	MEM_bge_taken <= bge_taken;
  end
  
  // ######################### ms4 end
  
  // ######################### ms4 start WB
  
  always @(posedge clk)
  begin
	WB_aluout <= MEM_aluout;
	WB_rd <= MEM_rd;
	WB_pc <= MEM_pc;
	WB_MemRdata <= MemRdata;
	WB_regwrite <= MEM_regwrite;
	WB_memtoreg <= MEM_memtoreg;
	WB_jal <= MEM_jal;
	WB_jalr <= MEM_jalr;
  end
  
  // ######################### ms4 end
  
  // ######################### ms4 start Forwarding
  
  always @(*)
  begin
    if (EX_rd == rs1 && ~EX_memwrite && EX_rd != 5'b0) rs1_forward = aluout;
    else if (MEM_rd == rs1 && MEM_rd != 5'b0 && MEM_memread) rs1_forward = MemRdata;
    else if (MEM_rd == rs1 && MEM_rd != 5'b0 && ~MEM_memread)  rs1_forward = MEM_aluout;
    else if (WB_rd == rs1 && WB_rd != 5'b0) rs1_forward = rd_data;
    else rs1_forward = rs1_data;
  end

  always @(*)
  begin
    if (EX_rd == rs2 && ~EX_memwrite && EX_rd != 5'b0) rs2_forward = aluout;
    else if (MEM_rd == rs2 && MEM_rd != 5'b0 && MEM_memread) rs2_forward = MemRdata;
    else if (MEM_rd == rs2 && MEM_rd != 5'b0 && ~MEM_memread)  rs2_forward = MEM_aluout;
    else if (WB_rd == rs2 && WB_rd != 5'b0) rs2_forward = rd_data;
    else rs2_forward = rs2_data;
  end
  
  
  always @(*)
  begin
	if((EX_rd == rs1 || EX_rd == rs2) && EX_memread && EX_rd != 0) enable = 0;
	else enable = 1;
  end

  // ######################### ms4 end

  // ############################ ms5 start
  always @(*)
  begin
  // ############################ ms6 start
  if(beq_taken | blt_taken | bgeu_taken | bne_taken | EX_jal | EX_jalr | bltu_taken | bge_taken ) bubble = 1;
  // ############################ ms6 end
  else bubble = 0;
  end
  
  // ############################ ms5 end
  
  
  // 
  // Register File 
  //
  // ########################### ms4 start
  regfile i_regfile(
    .clk			(clk),
    .we			(WB_regwrite),
    .rs1			(rs1),
    .rs2			(rs2),
    .rd			(WB_rd),
    .rd_data	(rd_data),
    .rs1_data	(rs1_data),
    .rs2_data	(rs2_data));


	assign MemWdata = MEM_rs2_data;

  // ########################### ms4 end
	
	//
	// ALU 
	//
	alu i_alu(
	// ########################### ms4 start
		.a			(EX_alusrc1),
		.b			(EX_alusrc2),
		.alucont	(EX_alucontrol),
	// ########################### ms4 end
		.result	(aluout),
		.N			(Nflag),
		.Z			(Zflag),
		.C			(Cflag),
		.V			(Vflag));

	
	always@(*)
	begin
	// ########################### ms4 start
		if      (auipc)	alusrc1[31:0]  =  ID_pc;
	// ########################### ms4 end
		else if (lui) 		alusrc1[31:0]  =  32'b0;
		else          			alusrc1[31:0]  =  rs1_forward[31:0];
	end
	
	// 2nd source to ALU (alusrc2)
	always@(*)
	begin
		if	     (auipc | lui)			alusrc2[31:0] = auipc_lui_imm[31:0];
		else if (alusrc & memwrite)	alusrc2[31:0] = se_imm_stype[31:0];
		else if (alusrc)						alusrc2[31:0] = se_imm_itype[31:0];
		else											alusrc2[31:0] = rs2_forward[31:0];
	end
		
		
	assign se_imm_itype[31:0] = {{20{ID_inst[31]}},ID_inst[31:20]};
	assign se_imm_stype[31:0] = {{20{ID_inst[31]}},ID_inst[31:25],ID_inst[11:7]};
	assign auipc_lui_imm[31:0] = {ID_inst[31:12],12'b0};


	// Data selection for writing to RF
	always@(*)
	begin
	// #################### start
		if	     (WB_jal | WB_jalr)			rd_data[31:0] = WB_pc + 4;
	// #################### end
		else if (WB_memtoreg)	rd_data[31:0] = WB_MemRdata;
		else						rd_data[31:0] = WB_aluout;
	end
	
endmodule
