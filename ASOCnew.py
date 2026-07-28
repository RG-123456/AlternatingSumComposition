def main():
    try:
        max_order = int(
            input("Enter the highest moment order: ")
        )

        if max_order < 0:
            print("Please enter a nonnegative integer.")
            return

        calculate_moments(max_order)

    except ValueError:
        print("Please enter a valid integer.")



def add_polynomials(p, q):
    """
    Add two polynomials.

    A polynomial is stored from low degree to high degree.
    Example:
        [-2, 3] represents 3n - 2
        [0, -2, 3] represents 3n^2 - 2n
    """
    length = max(len(p), len(q))
    result = [0] * length

    for i, value in enumerate(p):
        result[i] += value

    for i, value in enumerate(q):
        result[i] += value

    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return result


def multiply_by_linear(poly, constant):
    """
    Multiply a polynomial by:

        n + constant

    In this project, we need:
        n - 1 - k

    so constant = -1 - k.
    """
    result = [0] * (len(poly) + 1)

    for degree, coefficient in enumerate(poly):
        # Multiply by the constant part
        result[degree] += constant * coefficient

        # Multiply by n
        result[degree + 1] += coefficient

    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return result


def multiply_by_number(poly, number):
    """Multiply every coefficient by a number."""
    return [number * coefficient for coefficient in poly]


def polynomial_to_string(poly):
    """Convert a polynomial list into readable mathematical form."""
    terms = []

    for degree in range(len(poly) - 1, -1, -1):
        coefficient = poly[degree]

        if coefficient == 0:
            continue

        sign = "-" if coefficient < 0 else "+"
        absolute_value = abs(coefficient)

        if degree == 0:
            term = str(absolute_value)
        elif degree == 1:
            if absolute_value == 1:
                term = "n"
            else:
                term = f"{absolute_value}n"
        else:
            if absolute_value == 1:
                term = f"n^{degree}"
            else:
                term = f"{absolute_value}n^{degree}"

        terms.append((sign, term))

    if not terms:
        return "0"

    first_sign, first_term = terms[0]
    result = first_term if first_sign == "+" else f"-{first_term}"

    for sign, term in terms[1:]:
        result += f" {sign} {term}"

    return result

def apply_recurrence_matrix(coefficient_vector):
    """
    Apply one recurrence-matrix step:

        c^(m+1) = A c^(m)

    based on

        D(e_k) = e_k + (n-1-k)e_(k+1) + k e_(k-1).

    Each entry of coefficient_vector is a polynomial in n.
    """

    # After one application of D, the highest possible index
    # increases by at most one.
    new_vector = [[0] for _ in range(len(coefficient_vector) + 1)]

    for k, polynomial in enumerate(coefficient_vector):

        # 1. Diagonal contribution:
        #    coefficient of e_k goes to e_k
        new_vector[k] = add_polynomials(
            new_vector[k],
            polynomial
        )

        # 2. Lower-diagonal contribution:
        #    coefficient of e_k contributes
        #    (n - 1 - k) times to e_(k+1)
        upward_part = multiply_by_linear(
            polynomial,
            constant=-1-k
        )

        new_vector[k + 1] = add_polynomials(
            new_vector[k + 1],
            upward_part
        )

        # 3. Upper-diagonal contribution:
        #    coefficient of e_k contributes
        #    k times to e_(k-1)
        if k > 0:
            downward_part = multiply_by_number(
                polynomial,
                k
            )

            new_vector[k - 1] = add_polynomials(
                new_vector[k - 1],
                downward_part
            )

    return new_vector

def calculate_moments(max_order):
    """
    Calculate E_0^c(n), E_1^c(n), ..., E_max_order^c(n).

    Basis:
        e_k = y u^(n-1-k) v^k

    Recurrence:
        D(e_k) = e_k + (n-1-k)e_(k+1) + k e_(k-1)
    """

    # Initial coefficient vector:
    # F_0 = e_0
    coefficient_vector = [[1]]

    all_moments = [[1]]

    print("\nOrder 0")
    print("Coefficient vector:")
    print(["1"])
    print("E_0^c(n) = 1")

    for order in range(1, max_order + 1):
        coefficient_vector = apply_recurrence_matrix(coefficient_vector)

        # At y = 1, v = 0.
        # Therefore only the first coefficient remains.
        moment = coefficient_vector[0]
        all_moments.append(moment)

        print(f"\nOrder {order}")
        print("Coefficient vector:")

        readable_vector = [
            polynomial_to_string(poly)
            for poly in coefficient_vector
        ]

        print(readable_vector)

        print(
            f"E_{order}^c(n) = "
            f"{polynomial_to_string(moment)}"
        )

    print("\n" + "=" * 50)
    print("All moments")
    print("=" * 50)

    for order, moment in enumerate(all_moments):
        print(
            f"E_{order}^c(n) = "
            f"{polynomial_to_string(moment)}"
        )



if __name__ == "__main__":
    main()