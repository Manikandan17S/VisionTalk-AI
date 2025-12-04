# ai/brain.py
import subprocess
import shlex
import time

BRIEFING_PREFIX = (
    "You are JARVIS, an assistant. By default respond concisely (2-3 short lines). "
    "Only give long/detailed explanations when the user explicitly requests 'explain in detail', "
    "'long answer', or 'go deep'. Do NOT print internal commentary like 'User question with...' "
    "or meta-statements. Answer clearly and directly."
)

def _call_ollama_with_prompt(full_prompt, timeout=90):
    """
    Run the ollama CLI in a safe, list-argument way and return subprocess.CompletedProcess.
    We pass the prompt as a single argument to avoid shell quoting problems.
    """
    # Build command as list (avoids shell quoting issues)
    cmd = ["ollama", "run", "phi3:mini", full_prompt]
    print(f"[AI][DEBUG] Running command: {' '.join(shlex.quote(p) for p in cmd[:3])} <PROMPT_ARG_TRUNCATED>")
    # NOTE: we avoid shell=True and pass the prompt as an argument
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=timeout
    )

def ai_respond(prompt):
    """Get response from Ollama AI (offline) with brevity instruction and a retry for meta replies."""
    full_prompt = f"{BRIEFING_PREFIX}\n\nUser: {prompt}\nAssistant:"
    # debug print of what we send (first 500 chars)
    print(f"[AI] Full prompt (start): {full_prompt[:500]!r}")

    try:
        # first attempt
        result = _call_ollama_with_prompt(full_prompt, timeout=90)
        print(f"[AI] Return code: {result.returncode}")

        if result.returncode == 0 and result.stdout:
            answer = result.stdout.strip()
            answer = ''.join(c for c in answer if ord(c) >= 32 or c in '\n\t')
            print(f"[AI] Got response (start): {answer[:300]}...")

            # Defensive check: sometimes model returns a meta-prefixed reply (e.g. "User question with ...")
            # If that looks like a meta reply, retry once with a simpler explicit prompt.
            meta_indicators = ["user question with", "user asked", "assistant reply", "heuristic approach"]
            lower_ans = answer.lower()
            if any(ind in lower_ans for ind in meta_indicators) and len(answer.split()) > 6:
                print("[AI] Detected meta-like or unrelated response. Retrying once with a simpler prompt.")
                retry_prompt = f"Answer concisely and directly (2-3 short lines): {prompt}"
                retry_full = f"{BRIEFING_PREFIX}\n\nUser: {retry_prompt}\nAssistant:"
                retry_result = _call_ollama_with_prompt(retry_full, timeout=90)
                if retry_result.returncode == 0 and retry_result.stdout:
                    retry_answer = retry_result.stdout.strip()
                    retry_answer = ''.join(c for c in retry_answer if ord(c) >= 32 or c in '\n\t')
                    print(f"[AI] Retry response (start): {retry_answer[:300]}...")
                    return retry_answer
                else:
                    print(f"[AI] Retry failed or empty. Stderr: {retry_result.stderr[:200] if retry_result.stderr else 'None'}")
                    return answer  # fall back to original even if meta
            else:
                return answer if answer else "I'm processing that, please try again."
        else:
            print(f"[AI] Empty response or error. Stderr: {result.stderr[:300] if result.stderr else 'None'}")
            return "I need a moment to process that. Please try again."

    except subprocess.TimeoutExpired:
        print("[AI] ⏱️ TIMEOUT - AI took too long to respond")
        return "I'm thinking too hard on that one. Please try a simpler question."

    except Exception as ex:
        print(f"[AI] ❌ Error calling Ollama: {ex}")
        return f"Error occurred. Let me try again."
