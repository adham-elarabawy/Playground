import argparse

#--CONFIG--#
low_shift = 10
high_shift = 70

cutoff_thresh = 280

APPLY_DYNAMIC_SHIFT = True


parser = argparse.ArgumentParser(
    description='Calculate how far to pull back ballista for a specified distance.')
parser.add_argument('--dist', dest='distance',
                    help='(INCHES) Desired distance for the tennis ball to land at.', required=True, type=float),

args = parser.parse_args()


def apply_shift(distance):
    if APPLY_DYNAMIC_SHIFT:
        if distance >= cutoff_thresh:
            return distance + high_shift
        if distance < cutoff_thresh:
            return distance + low_shift
    else:
        return distance + low_shift


def raw_calculate(distance):
    return 0.67 * (distance) ** 0.418


raw_in = args.distance
effective_distance = apply_shift(args.distance)
raw_output = raw_calculate(effective_distance)
output = round(raw_output, 1)

print(
    f'Info:\n   raw input = {raw_in}\n   shifted = {effective_distance}\n   applied dynamic shift = {APPLY_DYNAMIC_SHIFT}')
print(f'PULL BACK: {output} inches')
