# TODO: Validate
"""How a download is named in the log.

An endpoint is a method on the client rather than a class of its own, so the
name a request is logged under comes from the method that made it rather than
from anything the caller has to pass in.
"""

from __future__ import annotations

from inspect import Parameter, signature
from typing import Any, Protocol


# TODO: Validate
class NamedCallable(Protocol):
    """A callable that knows the name it was defined under.

    A plain `Callable` does not carry `__name__`, and the name is the whole
    point here: it is what a request is logged under.
    """

    @property
    def __name__(self) -> str: ...

    # A method of any signature is what this stands for, so its arguments
    # and its answer are whatever that method's are.
    def __call__(self, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        ...


# TODO: Validate
def non_default_args(
    func: NamedCallable,
    values: dict[str, Any],
) -> dict[str, Any]:
    """Return the args that are changed from their default values."""
    return {
        name: values[name]
        for name, param in signature(func).parameters.items()
        if param.default is not Parameter.empty
        and name in values
        and values[name] != param.default
    }


# TODO: Validate
def get_log_id(func: NamedCallable, values: dict[str, Any]) -> str:
    """Get the log id.

    Example: method_name (arg1='value1' arg2='value2')
    """
    required = {
        name: values[name]
        for name, param in signature(func).parameters.items()
        if param.default is Parameter.empty and name in values
    }
    set_args = {**required, **non_default_args(func, values)}
    parts = [f"{name}={value!r}" for name, value in set_args.items()]
    name = func.__name__
    if not parts:
        return name
    return f"{name} ({' '.join(parts)})"
