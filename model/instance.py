import re
from pydantic import ValidationInfo

# Compile the regex pattern once
OBJECT_TAG_PATTERN = re.compile(
    r'\$\(\s*([a-zA-Z0-9_-]+)\s*#\s*([a-zA-Z0-9_-]+)\s*\)'
)

class Instance(str):
    """
    Akceptowane formy
      *kind:role #id
      *kind:role #$id
      *kind:role #$id.#  itd.

    Części:
      *         – opcjonalna gwiazdka (aktor)
      kind      – wymagany typ
      :role     – opcjonalna rola
      #id[.#]   – opcjonalny identyfikator
                  $…   → reference = True
                  ….# → hashed_reference = True
    """

    _pattern = re.compile(r"""
        ^\s*
        (?P<actor>\*)?                     # gwiazdka
        \s*
        (?P<type>[A-Za-z_-]+)              # kind
        \s*
        (?: : \s* (?P<role>[A-Za-z_-]+) )? # :role
        \s*
        (?: \# \s* (?P<id>[^\s#]+) \s* \#? )? # #id (bez spacji i kolejnych #)
        \s*$
    """, re.VERBOSE)

    _split = re.compile(r'[:#]')

    # ── walidacja pydantic ─────────────────────────────────────
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str, info: ValidationInfo | None = None):
        if v is None:
            raise ValueError(f"Instance has none value.")
        if not re.match(cls._pattern, v):
            raise ValueError(f"Invalid Instance string format: {v!r}")
        return cls(v)

