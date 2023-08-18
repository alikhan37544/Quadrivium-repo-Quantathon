import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.circuit.library import ZZFeatureMap
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.components.feature_maps import FirstOrderExpansion


X, y = make_classification(n_samples=100, n_features=1, n_informative=1, n_redundant=0, random_state=42)
X = X.flatten()



feature_map = ZZFeatureMap(2, reps=1)


quantum_instance = QuantumInstance(Aer.get_backend('qasm_simulator'), shots=1024)
qsvm = QSVM(feature_map, None, None)
result = qsvm.run(quantum_instance)

quantum_features = result['svm']['support_vectors']


combined_data = np.column_stack((X, quantum_features))


logreg = LogisticRegression()
logreg.fit(combined_data, y)


x_vals = np.linspace(np.min(X), np.max(X), 100)
y_probs = logreg.predict_proba(np.column_stack((x_vals, np.zeros_like(x_vals))))[:, 1]


plt.scatter(X, y, label='Data')
plt.plot(x_vals, y_probs, color='red', label='Logistic Regression')
plt.xlabel('Supply')
plt.ylabel('Food Cost')
plt.title('Food Cost vs. Supply')
plt.legend()
plt.show()
