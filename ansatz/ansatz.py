from qiskit.circuit import QuantumCircuit, ParameterVector


def apply_ansatz(qc: QuantumCircuit, params: ParameterVector, reps: int) -> None:
    """Applies a gate sequence that defines the ansatz.

    Args:
        qc (QuantumCircuit): The encoded quantum circuit.
        params (ParameterVector): Parameters that will be optimized.
        reps (int): The number of repetitions.
    """
    for i in range(reps):
        
        qc.cx(control_qubit = qc.qregs[0][0], target_qubit = qc.qregs[0][1])
        qc.ry(theta = params[4*i], qubit = qc.qregs[0][0])
        qc.ry(theta = params[4*i+1], qubit = qc.qregs[0][1])
        qc.cx(control_qubit = qc.qregs[0][1], target_qubit = qc.qregs[0][0])
        qc.ry(theta = params[4*i+2], qubit = qc.qregs[0][0])
        qc.ry(theta = params[4*i+3], qubit = qc.qregs[0][1])
        qc.barrier()