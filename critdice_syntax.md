# CritDice Syntax

## Dice Rolling: XdY
    X = Number of dice to roll.
    Y = Number of sides on each die.
    Example: 4d6 (roll four 6-sided dice).

## Custom Dice: dN
    N = Any number between 1 and 999999999 for custom dice sides.
    Example: d100 (roll a 100-sided die).

## Fate/Fudge Dice: dF
    Results in -1, 0, +1.
    Example: 4dF (roll four Fate/Fudge dice).

## Keep Highest/Lowest: K or k
    K (uppercase) followed by a number = Keep highest rolls.
    k (lowercase) followed by a number = Keep lowest rolls.
    Without a number, keep the single highest or lowest roll.
    Example: 5d10K3 (roll five 10-sided dice, keep the three highest).

## Drop Highest/Lowest: X or x
    X (uppercase) followed by a number = Drop highest rolls.
    x (lowercase) followed by a number = Drop lowest rolls.
    Example: 5d10X2 (roll five 10-sided dice, drop the two highest).

## Reroll: R or r
    R (uppercase) = Reroll specified values indefinitely.
    r (lowercase) = Reroll specified values once.
    Follow with a condition for rerolling (e.g., ≤4).
    Example: 6d6R1 (roll six 6-sided dice, reroll 1s indefinitely).

## Exploding Dice: !
    A die is rolled again and added to the total if it rolls its maximum value or meets specified condition.
    Example: 3d6! (roll three 6-sided dice, explode on 6s).

## Compounding Dice: !!
    Similar to exploding, but additional rolls are compounded into a single result.
    Example: 3d6!! (roll three 6-sided dice, compound on 6s).

## Penetrating Dice: !p
    Similar to exploding, but each additional roll subtracts 1 from its result.
    Example: 3d6!p (roll three 6-sided dice, penetrate on 6s).

## Count Successes/Failures: ≥, ≤, f
    ≥ or ≤ followed by a number = Count rolls as successes or failures.
    f specifies failure conditions, subtracting from successes.
    Example: 8d10≥5f≤3 (roll eight 10-sided dice, count ≥5 as success, ≤3 as failure).

## Arithmetic Operations: +, -
    Perform simple arithmetic operations.
    Example: 4d6+10 (roll four 6-sided dice, add 10 to the total).
