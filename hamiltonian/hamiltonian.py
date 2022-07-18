from qiskit.opflow import PauliSumOp
from qiskit_nature.drivers.second_quantization.pyscfd import PySCFDriver
from qiskit_nature.problems.second_quantization.electronic import ElectronicStructureProblem
from qiskit_nature.mappers.second_quantization import ParityMapper
from qiskit_nature.converters.second_quantization.qubit_converter import QubitConverter


def hamiltonian_qubit_op(dist: float) -> PauliSumOp:
    """_summary_

    Args:
        dist (float): The distance between atoms.

    Returns:
        PauliSumOp: _description_
    """
    
    molecule = "H .0 .0 .0; H .0 .0 " + str(dist)
    driver = PySCFDriver(atom = molecule)
    qmolecule = driver.run()
    
    problem = ElectronicStructureProblem(driver = driver)
    
    second_q_ops = problem.second_q_ops()
    
    main_op = second_q_ops[0]
    mapper = ParityMapper()
    converter = QubitConverter(mapper = mapper, two_qubit_reduction = True)
    
    num_particles = problem.num_particles
    qubit_op = converter.convert(main_op, num_particles = num_particles)
    
    return qubit_op
    