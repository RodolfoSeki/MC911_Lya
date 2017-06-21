class VirtualMachine(object):
  def __init__(self, code, memsize=100000, scopes=100, string_list=[]):
    self.pc = 0
    self.M = [0]*memsize
    self.D = [0]*scopes
    self.H = string_list
    self.label = dict()
    self.code = code
    
    self.get_label()
    #print(self.label)
    self.run()
  
  def get_label(self):
    
    for i, item in enumerate(self.code):
      if item[0] == 'lbl':
        
        self.code[i] = ('nop',)
        self.label[item[1]] = i
        

  def exec_inst(self,inst):
    print ('Instruction: ', inst)
    method = 'eval_' + inst[0]
    execute = getattr(self, method, None)
    if execute is not None:
      execute(inst)
      print ('PC:{}  SP:{}'.format(self.pc, self.sp))
    else:
      raise Exception('No instruction of type {}'.format(inst[0]))
  
  def get_instruction(self, i):
    #print("i: ", i, "  ", self.code[i])
    return self.code[i]  
  
  def run(self):
    while self.pc < len(self.code):
      instruct = self.get_instruction(self.pc)
      #print("M: ", self.M)
      #print("D: ", self.D)
      self.exec_inst(instruct)
  

  def eval_ldc(self, inst):
    '''
    ("ldc", k)     # Load constant
            sp=sp+1;  M[sp]=k
    '''
    k = inst[1]
    self.sp += 1
    self.M[self.sp] = k
    self.pc = self.pc + 1

  def eval_ldv(self, inst):
    '''
    ("ldv", i, j)  # Load value
        sp=sp+1;  M[sp]=M[D[i]+j]
    '''
    i, j = inst[1], inst[2]
    self.sp += 1
    self.M[self.sp] = self.M[self.D[i] + j]
    self.pc = self.pc + 1

  def eval_ldr(self, inst):
    '''
    ("ldr", i, j)  # Load reference
          sp=sp+1;  M[sp]=D[i]+j
    '''
    i, j = inst[1], inst[2]
    self.sp += 1
    self.M[self.sp] = self.D[i] + j
    self.pc = self.pc + 1

  def eval_stv(self, inst):
    '''
    ("stv", i, j)  # Store value
          M[D[i]+j]=M[sp];  sp=sp-1
    '''
    i, j = inst[1], inst[2]
    self.M[self.D[i] + j] = self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_lrv(self, inst):
    '''
    ("lrv", i, j)  # Load reference value
          sp=sp+1;  M[sp]=M[M[D[i]+j]]
    '''
    i, j = inst[1], inst[2]
    self.sp += 1
    self.M[self.sp] = self.M[self.M[self.D[i] + j]]
    self.pc = self.pc + 1

  def eval_srv(self, inst):
    '''
    ("srv", i, j)  # Store reference value
          M[M[D[i]+j]]=M[sp];  sp=sp-1
    '''
    i, j = inst[1], inst[2]
    self.M[self.M[self.D[i] + j]] = self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_add(self, inst):
    '''
    ("add")        # Add
          M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
    '''
    self.M[self.sp - 1] = self.M[self.sp - 1] + self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_sub(self, inst):
    '''
    ("sub")        # Subtract
          M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
    '''
    self.M[self.sp - 1] = self.M[self.sp - 1] - self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_mul(self, inst):
    '''
    ("mul")        # Multiply
          M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
    '''
    self.M[self.sp - 1] = self.M[self.sp - 1] * self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_div(self, inst):
    '''
    ("div")        # Division
          M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
    '''
    self.M[self.sp - 1] = self.M[self.sp - 1] / self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_mod(self, inst):
    '''
    ("mod")        # Modulus
          M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
    '''
    self.M[self.sp - 1] = self.M[self.sp - 1] % self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1

  def eval_neg(self, inst):
    '''
    ("neg")        # Negate
          M[sp]= -M[sp]
    '''
    self.M[self.sp] = -self.M[self.sp]
    self.pc = self.pc + 1

  def eval_abs(self, inst):
    '''
    ('abs')        # Absolute Value
          M[sp]= abs(M[sp])
    '''
    self.M[self.sp] = abs(self.M[self.sp])
    self.pc = self.pc + 1

  def eval_and(self, inst):
    '''
    ("and")        # Logical And
          M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
    '''
    self.M[self.sp - 1] = self.M[self.sp - 1] and self.M[self.sp]
    self.sp -= 1
    self.pc = self.pc + 1
  
  def eval_lor(self,inst):
    '''
    ("lor")        # Logical Or
                      M[sp-1]=M[sp-1] or M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] or self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
  
  def eval_not(self,inst):
    '''
    ("not")        # Logical Not
                      M[sp]= not M[sp]
    '''
    
    self.M[self.sp]= not self.M[self.sp]
    
    self.pc += 1
  
  def eval_les(self,inst):
    '''
    ("les")        # Less
                      M[sp-1]=M[sp-1] < M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] < self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
    
  def eval_leq(self,inst):
    '''
    ("leq")        # Less or Equal
                      M[sp-1]=M[sp-1] <= M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] <= self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
  
  def eval_grt(self,inst):
    '''
    ("grt")        # Greater
                      M[sp-1]=M[sp-1] > M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] > self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
    
  def eval_gre(self,inst):
    '''
    ("gre")        # Greater or Equal
                      M[sp-1]=M[sp-1] >= M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] >= self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
  
  
  def eval_equ(self,inst):
    '''
    ("equ")        # Equal
                      M[sp-1]=M[sp-1] == M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] == self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
    
  
    
  def eval_neq(self,inst):
    '''
    ("neq")        # Not Equal
                      M[sp-1]=M[sp-1] != M[sp];  sp=sp-1
    '''
    
    self.M[self.sp-1]= self.M[self.sp-1] != self.M[self.sp]
    self.sp -= 1
    
    self.pc += 1
  
  def eval_jmp(self,inst):
    '''
    ("jmp", p)     # Jump
                      pc=p
    '''
    p = self.label[inst[1]]
    self.pc = p
  
  def eval_jof(self,inst):
    '''
    ("jof", p)     # Jump on False
                      if not M[sp]:
                          pc=p
                      else:
                          pc=pc+1
                      sp=sp-1
    '''
    p = self.label[inst[1]]
    
    if not self.M[self.sp]:
      self.pc = p
    else:
      self.pc += 1
    self.sp -= 1
    
  
  
  def eval_alc(self, inst):
    '''
    ("alc", n)     # Allocate memory
                      sp=sp+n
    '''
    n = inst[1]
    #self.M = [0] * n
    
    self.sp += n
    self.pc += 1
  
  
  def eval_dlc(self, inst):
    '''
    ("dlc", n)     # Deallocate memory
                      sp=sp-n
    '''
    n = inst[1]
    
    self.sp -= n
    self.pc += 1
  

  def eval_cfu(self,inst):
    '''
    ("cfu", p)     # Call Function
                      sp=sp+1; M[sp]=pc+1; pc=p
    '''
    p = self.label[inst[1]]
    
    self.sp += 1
    self.M[self.sp] = self.pc+1
    self.pc = p

  
  def eval_enf(self,inst):
    '''
    ("enf", k)     # Enter Function
                      sp=sp+1; M[sp]=D[k]; D[k]=sp+1
    '''
    k = inst[1]
    
    self.sp += 1
    self.M[self.sp] = self.D[k]
    self.D[k] = self.sp + 1

    self.pc += 1
  
  
  
  def eval_ret(self,inst):
    '''
    ("ret", k, n)  # Return from Function
                      D[k]=M[sp]; pc=M[sp-1]; sp=sp-(n+2)
    '''
    k = inst[1]
    n = inst[2]
    
    self.D[k] = self.M[self.sp]
    self.pc = self.M[self.sp-1]
    self.sp = self.sp - (n+2)

  
  def eval_idx(self,inst):
    '''
    ("idx", k)    # Index
                    M[sp-1]=M[sp-1] + M[sp] * k
                    sp=sp-1
    '''
    k = inst[1]
    self.M[self.sp-1]=self.M[self.sp-1] + self.M[self.sp] * k
    self.sp -= 1

    self.pc += 1
  
  def eval_grc(self,inst):
    '''
    ("grc")        # Get(Load) Reference Contents
                      M[sp]=M[M[sp]]
    '''
    self.M[self.sp]=self.M[self.M[self.sp]]

    self.pc += 1
  
  
  def eval_lmv(self,inst):
    '''
    ("lmv", k)     # Load multiple values
                        t=M[sp]
                        M[sp:sp+k]=M[t:t+k]
                        sp += (k-1)
    '''
    k = inst[1]
    
    t= self.M[self.sp]
    self.M[self.sp:self.sp+k] = self.M[t:t+k]
    self.sp += (k-1)

    self.pc += 1
  
  
  def eval_smv(self,inst):
    '''
    ("smv", k)     # Store multiple Values
                        t = M[sp-k]
                        M[t:t+k] =M[sp-k+1:sp+1]
                        sp -= (k+1)
    '''
    k = inst[1]
    
    t = self.M[self.sp-k]
    self.M[t:t+k] = self.M[self.sp-k+1:self.sp+1]
    self.sp -= (k+1)
    
    self.pc += 1
    
  
  def eval_smr(self,inst):
    '''
    ("smr", k)     # Store multiple References
                        t1 = M[sp-1]
                        t2 = M[sp]
                        M[t1:t1+k] = M[t2:t2+k]
                        sp -= 1
    '''
    k = inst[1]
    
    t1 = self.M[self.sp-1]
    t2 = self.M[self.sp]
    self.M[t1:t1+k] = self.M[t2:t2+k]
    self.sp -= 1
    
    self.pc += 1
  
  def eval_sts(self,inst):
    '''
    ("sts", k)     # Store string constant on reference
                   adr=M[sp]
                   M[adr]=len(H[k])
                   for c in H[k]:
                       adr=adr+1
                       M[adr]=c;
                   sp=sp-1
    '''
    k = inst[1] 
    adr = self.M[self.sp]
    self.M[adr] = len(self.H[k])
    for c in self.H[k]:
        adr=adr+1
        self.M[adr]=c;
    self.sp -= 1
    self.pc += 1
  
  def eval_rdv(self,inst):
    '''
    ("rdv")     # Read single Value
                sp=sp+1;  M[sp]=input()
    '''
    self.sp += 1
    self.M[self.sp] = int(input())
    
    self.pc += 1
  
  
  def eval_rds(self,inst):
    '''
    ("rds")    # Read String and store it on stack reference
               str=input()
               adr=M[sp]
               M[adr] = len(str)
               for k in str:
                   adr=adr+1
                   M[adr]=k
               sp=sp-1
    '''
    string=input()
    adr=self.M[self.sp]
    self.M[adr] = len(string)
    
    for k in string:
      adr=adr+1
      self.M[adr]=k
    
    self.sp -= 1
    self.pc += 1
  
  def eval_prv(self,inst):
    '''
    ("prv", ischar) # Print Value (char or int)
                    if ischar:
                        print(chr(M[sp])
                    else:
                        print(M[sp]);
                    sp=sp-1
    '''
    ischar = False if len(inst) == 1 else inst[1]
    if ischar:
        print(chr(self.M[self.sp]))
    else:
        print(self.M[self.sp])
    self.sp -= 1
    self.pc += 1
    
    
  def eval_prt(self,inst):
    '''
    ('prt', k)      # Print Multiple Values
                    print(M[sp-k+1:sp+1]);
                    sp-=(k-1)
    '''
    k = inst[1]
    
    print(self.M[self.sp-k+1:self.sp+1])
    self.sp -= (k-1)
    self.pc += 1
    
  def eval_prc(self,inst):
    print(self.H[inst[1]],end="")
    self.pc += 1
    
  def eval_prs(self,inst):
    ''' 
    adr = M[sp]
    len = M[adr]
    for i in range(0,len):
        adr = adr + 1
        print(M(adr),end="")
        sp=sp-1
    '''
    adr = self.M[self.sp]
    length = self.M[adr]
    for i in range(length):
      adr = adr + 1
      print(self.M[adr],end="")
      self.sp -= 1
    self.pc += 1
    
  def eval_stp(self,inst):
    self.sp = -1
    self.D[0] = 0
    self.pc += 1
    
  def eval_nop(self,inst):
    self.pc += 1
    pass
        
  def eval_end(self,inst):
    self.pc += 1
    pass
