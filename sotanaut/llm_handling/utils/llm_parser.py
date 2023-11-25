import re
from typing import List


class LLMParser:
    @staticmethod
    def merge_prompts(*prompts: str, separator="\n") -> str:
        """Merges multiple prompt strings into one.

        Args:
            *prompts: Variable length prompt list.
            separator (str): The separator to use between prompts.

        Returns:
            str: A single merged prompt string.
        """
        valid_prompts = [prompt for prompt in prompts if prompt]
        return separator.join(valid_prompts)

    @staticmethod
    def parse_csv_output(output: str, max_entries: int = 10) -> List[str]:
        """Parses the LLM output assumed to be in a CSV format. Extracts entries from a CSV list,
        handling both formatted and plain list outputs.

        Args:
            output (str): The string output from the LLM.
            max_entries (int): Maximum number of entries to return.

        Returns:
            List[str]: A list of parsed entries.

        Raises:
            ValueError: If the output format is not as expected or if no valid data is found.
        """
        if not output:
            return []

        # Attempt to extract a CSV list from a formatted output
        start_index = output.find(":") + 1 if ":" in output else 0
        end_index = output.rfind(".", 0, output.rfind(",")) if "," in output else len(output)
        csv_part = output[start_index:end_index].strip()

        if not csv_part and "," not in output:
            raise ValueError(
                "Output does not contain a CSV format or is not in the expected format."
            )

        if entries := [entry.strip() for entry in csv_part.split(",") if entry.strip()]:
            return entries[:max_entries]
        else:
            raise ValueError("No valid entries found in the output.")

    @staticmethod
    def parse_enumerated_output(output: str, max_entries: int = 10) -> List[str]:
        """Parses the LLM output assumed to be in an enumerated format. Extracts entries from a
        list presented with numbers.

        Args:
            output (str): The string output from the LLM.
            max_entries (int): Maximum number of entries to return.

        Returns:
            List[str]: A list of parsed entries.

        Raises:
            ValueError: If no valid enumerated data is found.
        """
        if not output:
            return []

        # Regular expression to identify enumerated list items
        pattern = r"\d+[.)] +([^,]+)"
        matches = re.finditer(pattern, output)

        entries = [match.group(1).strip() for match in matches]

        if len(entries) == 0:
            raise ValueError("No valid enumerated entries found in the output.")

        entries = entries[:max_entries]
        return LLMParser.clean_list(entries)

    @staticmethod
    def clean_list(output: List[str]) -> List[str]:
        """Cleans and splits an enumerated output list.

        Args:
            output (List[str]): The output list containing a single string of enumerated items.

        Returns:
            List[str]: A list of cleaned and individual enumerated items.

        Raises:
            ValueError: If the output list is empty or not in the expected format.
        """
        if not output or not isinstance(output, list) or len(output) != 1:
            raise ValueError("Output is not in the expected list format.")

        # Extracting the single string from the list
        enumerated_string = output[0]

        # Splitting based on the newline character and removing any leading/trailing whitespace
        split_items = [item.strip() for item in enumerated_string.split("\n") if item.strip()]

        # Further cleaning if needed (e.g., removing numbers and periods)
        cleaned_items = [re.sub(r"^\d+\.\s*", "", item) for item in split_items]

        return cleaned_items
