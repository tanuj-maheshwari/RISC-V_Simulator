class BTB:
    def __init__(self):
        self.BranchTargets = {}
        self.JumpPCs = []

    def ispresent_btb(self, pc_value):
        if pc_value in self.BranchTargets:
            return True
        else:
            return False

    def isjump_btb(self, pc_value):
        if pc_value in self.JumpPCs:
            return True
        else:
            return False

    def add_to_btb(self, pc_value, branch_target, is_jump=False):
        self.BranchTargets[pc_value] = branch_target
        if is_jump:
            self.JumpPCs.append(pc_value)

    def target_from_btb(self, pc_value):
        return self.BranchTargets[pc_value]
