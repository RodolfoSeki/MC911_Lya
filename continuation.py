	def eval_ldc(self, inst):
	  '''
	  (’ldc’, k)     # Load constant
			sp=sp+1;  M[sp]=k
	  '''
		k = inst[1]
		self.sp += 1
		self.M[self.sp] = k
		self.pc = self.pc + 1
	
	def eval_ldv(self, inst):
		'''
    (’ldv’, i, j)  # Load value
                      sp=sp+1;  M[sp]=M[D[i]+j]
		'''
		i, j = inst[1], inst[2]
		self.sp += 1
    self.M[self.sp] = self.M[self.D[i] + j]
		self.pc = self.pc + 1

	def eval_ldr(self, inst):
		'''
    (’ldr’, i, j)  # Load reference
                      sp=sp+1;  M[sp]=D[i]+j
		'''
		i, j = inst[1], inst[2]
		self.sp += 1
    self.M[self.sp] = self.D[i] + j
		self.pc = self.pc + 1

	def eval_stv(self, inst):
		'''
    (’stv’, i, j)  # Store value
                      M[D[i]+j]=M[sp];  sp=sp-1
		'''
		i, j = inst[1], inst[2]
    self.M[self.D[i] + j] = self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_lrv(self, inst):
		'''
    (’lrv’, i, j)  # Load reference value
                      sp=sp+1;  M[sp]=M[M[D[i]+j]]
		'''
		i, j = inst[1], inst[2]
		self.sp += 1
		self.M[self.sp] = self.M[self.M[self.D[i] + j]]
		self.pc = self.pc + 1

	def eval_srv(self, inst):
		'''
    (’srv’, i, j)  # Store reference value
                      M[M[D[i]+j]]=M[sp];  sp=sp-1
		'''
		i, j = inst[1], inst[2]
		self.M[self.M[self.D[i] + j]] = self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_add(self, inst):
		'''
    (’add’)        # Add
                      M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
		'''
		self.M[self.sp - 1] = self.M[self.sp - 1] + self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_sub(self, inst):
		'''
    (’sub’)        # Subtract
                      M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
		'''
		self.M[self.sp - 1] = self.M[self.sp - 1] - self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_mul(self, inst):
		'''
    (’mul’)        # Multiply
                      M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
		'''
		self.M[self.sp - 1] = self.M[self.sp - 1] * self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_div(self, inst):
		'''
    (’div’)        # Division
                      M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
		'''
		self.M[self.sp - 1] = self.M[self.sp - 1] / self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_mod(self, inst):
		'''
    (’mod’)        # Modulus
                      M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
		'''
		self.M[self.sp - 1] = self.M[self.sp - 1] % self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1

	def eval_neg(self, inst):
		'''
    (’neg’)        # Negate
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
    (’and’)        # Logical And
                      M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
		'''
		self.M[self.sp - 1] = self.M[self.sp - 1] and self.M[self.sp]
		self.sp -= 1
		self.pc = self.pc + 1
