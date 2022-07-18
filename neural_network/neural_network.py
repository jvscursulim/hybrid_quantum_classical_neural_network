import numpy as np
from ansatz import apply_ansatz
from encoder import encode_data
from qiskit.circuit import ClassicalRegister, ParameterVector, QuantumCircuit, QuantumRegister
from qiskit.providers.aer import QasmSimulator


def neural_net(num_qubits: int, bond_length: float, parameters: ParameterVector, backend: QasmSimulator) -> QuantumCircuit:
    """Creates the neural network.

    Args:
        num_qubits (int): The number of qubits.
        bond_length (float): Bond length.
        backend (QasmSimulator): The qasm simulator.

    Returns:
        QuantumCircuit: The quantum circuit that represents the neural network.
    """
    
    qubits = QuantumRegister(size = num_qubits)
    bits = ClassicalRegister(size = num_qubits)
    
    qc = QuantumCircuit(qubits, bits)
    
    if len(parameters)%8 != 0:
        
        raise ValueError("Number of parameters should be multiples of 8!")
    
    params_per_layer = int(len(parameters)/2)
    params1 = ParameterVector(r"\theta_1", length = params_per_layer)
    params2 = ParameterVector(r"\theta_2", length = params_per_layer)
    
    qc_enc = encode_data(num_qubits = num_qubits, bond_length = bond_length)
    qc = qc.compose(other = qc_enc)
    
    reps_ansatz = int(len(params1)/4)
    apply_ansatz(qc = qc, params = params1, reps = reps_ansatz)
    
    qc.measure(qubit = qubits, cbit = bits)
    
    qc = qc.bind_parameters({params1:parameters[:params_per_layer]})
    
    job = backend.run(qc)
    result = job.result()
    
    count_dict = result.data()['counts']
    total_count = sum(count_dict.values())
    c_0 = 0
    c_2 = 0
    c_4 = 0
    c_6 = 0
    
    if '0x0' in count_dict.keys():
        
        c_0 = count_dict['0x0']
    if '0x2' in count_dict.keys():
        
        c_2 = count_dict['0x2']
    if '0x4' in count_dict.keys():
        
        c_4 = count_dict['0x4']
    if '0x6' in count_dict.keys():
        
        c_6 = count_dict['0x6']
        
    m_0_p_0 = (c_0 + c_4)/total_count
    m_0_p_1 = (c_2 + c_6)/total_count
    m_1_p_0 = (c_0 + c_2)/total_count
    m_1_p_1 = (c_4 + c_6)/total_count
    
    qc.reset(qubit = qubits)
    qc.h(qubit = qubits)
    qc.ry(theta = np.pi*(m_0_p_0 - m_0_p_1), qubit = qubits[0])
    qc.ry(theta = np.pi*(m_1_p_0 - m_1_p_1), qubit = qubits[1])
    
    apply_ansatz(qc = qc, params = params2, reps = reps_ansatz)
    qc = qc.bind_parameters({params2: parameters[params_per_layer:]})
    
    return qc