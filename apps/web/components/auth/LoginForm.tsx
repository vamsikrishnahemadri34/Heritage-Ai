"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/providers/AuthProvider";

export default function LoginForm() {
  const router = useRouter();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSigningIn, setIsSigningIn] = useState(false);

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (isSigningIn) {
      return;
    }

    if (!email.trim() || !password) {
      setErrorMessage("Please enter your email and password.");
      return;
    }

    setErrorMessage(null);
    setIsSigningIn(true);

    try {
      await login({
        email: email.trim(),
        password,
      });

      router.replace("/");
    } catch {
      setErrorMessage(
        "Unable to sign in. Check your email and password and try again.",
      );
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <section
      aria-label="HeritageAI email sign in"
      className="mx-auto w-full max-w-md rounded-3xl border border-white/10 bg-white/[0.04] p-8 shadow-2xl backdrop-blur-xl"
    >
      <div className="mb-8 text-center">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-amber-300/80">
          HERITAGEAI
        </p>

        <h2 className="text-3xl font-semibold tracking-tight text-white">
          Welcome back
        </h2>

        <p className="mt-3 text-sm leading-6 text-white/60">
          Sign in with your HeritageAI account.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label
            htmlFor="email"
            className="mb-2 block text-sm font-medium text-white/80"
          >
            Email
          </label>

          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) => {
              setEmail(event.target.value);

              if (errorMessage) {
                setErrorMessage(null);
              }
            }}
            disabled={isSigningIn}
            className="w-full rounded-xl border border-white/10 bg-white/[0.05] px-4 py-3 text-sm text-white outline-none transition placeholder:text-white/30 focus:border-amber-300/50 focus:ring-1 focus:ring-amber-300/30 disabled:opacity-60"
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="mb-2 block text-sm font-medium text-white/80"
          >
            Password
          </label>

          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) => {
              setPassword(event.target.value);

              if (errorMessage) {
                setErrorMessage(null);
              }
            }}
            disabled={isSigningIn}
            className="w-full rounded-xl border border-white/10 bg-white/[0.05] px-4 py-3 text-sm text-white outline-none transition placeholder:text-white/30 focus:border-amber-300/50 focus:ring-1 focus:ring-amber-300/30 disabled:opacity-60"
          />
        </div>

        {errorMessage ? (
          <p
            role="alert"
            className="rounded-xl border border-red-400/20 bg-red-400/5 px-4 py-3 text-center text-sm text-red-300"
          >
            {errorMessage}
          </p>
        ) : null}

        <button
          type="submit"
          disabled={isSigningIn}
          className="w-full rounded-xl bg-amber-300 px-5 py-3.5 text-sm font-semibold text-black transition hover:bg-amber-200 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSigningIn ? "Signing in..." : "Sign in"}
        </button>
      </form>

      <p className="mt-8 text-center text-xs leading-5 text-white/40">
        Sign in with your HeritageAI email and password.
      </p>
    </section>
  );
}
