<script lang="ts">
	function scrollIntoView({ target }) {
		const el = document.querySelector(target.getAttribute('href'));
		if (!el) return;
		el.scrollIntoView({
			behavior: 'smooth'
		});
	}
</script>

<nav class="top-0 sticky flex flex-row w-full justify-between h-28 items-center px-14">
	<h1 class="text-5xl font-cursive">The Fine Print</h1>

	<div class="flex flex-row gap-11 justify-end items-center text-xl">
		<a href="#how-it-works" on:click|preventDefault={scrollIntoView}>How It Works</a>
		<button
			class="flex flex-row bg-gradient-to-r max-h-12 from-blue-800 to-purple-800 rounded-xl pl-5 py-3 hover:scale-105 duration-200 items-center gap-4"
		>
			<span class="text-white font-semibold">Add to Firefox</span>
			<img src="firefox.svg" alt="Firefox logo" class="rotate-0 hover:rotate-45 duration-500" />
		</button>
	</div>
</nav>
