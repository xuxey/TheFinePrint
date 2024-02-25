<script lang="ts">
	let y: number;

	function scrollIntoView({ target }) {
		const el = document.querySelector(target.getAttribute('href'));
		if (!el) return;
		el.scrollIntoView({
			behavior: 'smooth'
		});
	}
</script>

<nav
	class="top-0 sticky z-10 flex flex-row w-full justify-between h-28 items-center px-14 duration-300 {y >
	20
		? 'bg-white'
		: 'bg-transparent'}"
>
	<a href="/" class="text-5xl font-cursive">The Fine Print</a>

	<div class="flex flex-row gap-11 justify-end items-center text-xl">
		<a class="hover:text-blue-800" href="/tryit">Try It</a>
		<a class="hover:text-blue-800" href="#how-it-works" on:click|preventDefault={scrollIntoView}
			>How It Works</a
		>
		<a
			href="/extension"
			class="flex flex-row bg-gradient-to-r max-h-12 from-blue-800 to-purple-800 rounded-xl pl-5 py-3 hover:scale-105 duration-200 items-center gap-4"
		>
			<span class="text-white font-semibold">Add to Firefox</span>
			<img src="firefox.svg" alt="Firefox logo" class="rotate-0 hover:rotate-45 duration-500" />
		</a>
	</div>
</nav>
<svelte:window bind:scrollY={y} />
