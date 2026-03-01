from discord import Interaction, app_commands
from discord.ext import commands

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

MAX_N = 10**12


def to_superscript(n: int) -> str:
    return str(n).translate(SUPERSCRIPT)


def prime_factors(n: int) -> list[tuple[int, int]]:
    """n を素因数分解し、(素数, 指数) のリストを返す"""
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            exp = 0
            while n % d == 0:
                exp += 1
                n //= d
            factors.append((d, exp))
        d += 1
    if n > 1:
        factors.append((n, 1))
    return factors


def format_factorization(factors: list[tuple[int, int]]) -> str:
    parts = []
    for prime, exp in factors:
        if exp == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}{to_superscript(exp)}")
    return "×".join(parts)


class Factorize(commands.Cog):
    """素因数分解 Cog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="factorize", description="正の整数を素因数分解します")
    @app_commands.describe(n="素因数分解する正の整数（2以上10¹²以下）")
    async def factorize_cmd(
        self,
        interaction: Interaction,
        n: app_commands.Range[int, 2, MAX_N],
    ) -> None:
        factors = prime_factors(n)
        result = format_factorization(factors)
        await interaction.response.send_message(f"{n} = {result}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Factorize(bot))
