from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from scipy.optimize import minimize
import os

app = Flask(__name__, static_folder="front_end", static_url_path="/")
CORS(app)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    Nc = data['Nc']
    Ns = data['Ns']
    fixed_values = data['fixed_values']

    matrix = solve_with_constraints(Ns, Nc, fixed_values)

    return jsonify({"matrix": matrix.tolist()})


def solve_with_constraints(Ns: int, Nc: int, fixed_values: list):
    num_vars = Ns * (Nc + 1)

    mask = np.ones(num_vars, dtype=bool)
    x0 = np.zeros(num_vars)

    for item in fixed_values:
        i, j, val = item['row'], item['col'], item['value']
        idx = i * (Nc + 1) + j
        mask[idx] = False
        x0[idx] = val

    for i in range(Ns):
        row_start = i * (Nc + 1)
        fixed_sum = 0.0
        free_indices = []
        for j in range(1, Nc + 1):
            idx = row_start + j
            if not mask[idx]:
                fixed_sum += x0[idx]
            else:
                free_indices.append(idx)

        num_free = len(free_indices)
        if num_free > 0:
            remain = 1.0 - fixed_sum
            for idx in free_indices:
                x0[idx] = remain / num_free

    def full_vector(x_free):
        x_full = x0.copy()
        x_full[mask] = x_free
        return x_full

    def loss(x_free):
        x = full_vector(x_free)
        matrix = x.reshape(Ns, Nc + 1)
        col0 = matrix[:, 0]
        loss_val = 0.0
        for j in range(1, Nc + 1):
            colj = matrix[:, j]
            dot = np.dot(col0, colj)
            loss_val += dot ** 2
        return loss_val

    constraints = []

    def constraint_col0(x_free):
        x = full_vector(x_free)
        matrix = x.reshape(Ns, Nc + 1)
        return np.sum(matrix[:, 0])
    constraints.append({'type': 'eq', 'fun': constraint_col0})

    for i in range(Ns):
        constraints.append({
            'type': 'eq',
            'fun': (lambda i: lambda x_free: np.sum(full_vector(x_free).reshape(Ns, Nc + 1)[i, 1:]) - 1)(i)
        })

    bounds = []
    for i in range(Ns):
        for j in range(Nc + 1):
            idx = i * (Nc + 1) + j
            if mask[idx]:
                if j == 0:
                    bounds.append((None, None))
                else:
                    bounds.append((0.0, 1.0))

    x_free0 = x0[mask]

    result = minimize(loss, x_free0, method='SLSQP', constraints=constraints, bounds=bounds)

    if not result.success:
        raise Exception(f"無法求解：{result.message}")

    x0[mask] = result.x
    matrix = x0.reshape(Ns, Nc + 1)
    return matrix


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
