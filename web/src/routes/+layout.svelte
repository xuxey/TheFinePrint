<script>
	import '../app.css';
	import Nav from '$lib/nav.svelte';
	import Footer from '../lib/footer.svelte';
</script>

<div class="bg-site2 bg-cover">
	<Nav />
	<div class="mx-20">
		<slot />
	</div>
	<Footer />
</div>
