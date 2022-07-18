from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister


def encode_data(num_qubits: int, bond_length: float) -> QuantumCircuit:
    """Encodes the data points in a quantum state.

    Args:
        num_qubits (int): The number of qubits.
        bond_length (float): Bond length.

    Returns:
        QuantumCircuit: The quantum state that represents the encoded data.
    """
    qubits = QuantumRegister(size = num_qubits, name = "qubits")
    bits = ClassicalRegister(size = num_qubits, name = "bits")
    
    qc = QuantumCircuit(qubits, bits)
    
    qc.h(qubit = qubits)
    qc.ry(theta = bond_length, qubit = qubits)
    
    return qc