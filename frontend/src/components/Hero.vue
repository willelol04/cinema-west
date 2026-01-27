<script setup>
    import { RouterLink } from 'vue-router';
    import Timeline from 'primevue/timeline';
    import Carousel from 'primevue/carousel';
    
    const upcomingPremieres = [
        {
            title: "Star wars: the last jedi",
            description: 'Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.',
            date: '2024-01-01',
            image: './src/assets/poster_examples/starwars.png',

        },
        {
            title: "Star wars: the last jedi",
            description: 'Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.',
            date: '2024-01-01',
            image: './src/assets/poster_examples/starwars.png',

        },
        {
            title: "Star wars: the last jedi",
            description: 'Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.',
            date: '2024-01-01',
            image: './src/assets/poster_examples/starwars.png',

        },
    ];
    
    


</script>

<template>
    <section>
    <h1>Kommande filmpremiärer:</h1>
    <Timeline class="timeline" :value="upcomingPremieres" layout="horizontal" align="middle">
        <div class="timeline-item">
            
        </div>
        <template #marker="slotProps">
            <RouterLink to="/movie/3">
            <div class="timeline-marker">
            <img :src="slotProps.item.image">
            <p>{{ slotProps.item.title }}</p>
            <p class="premiere">Premiär: {{ slotProps.item.date }}</p>
            </div>
            </RouterLink>
        </template>
        <template #content="slotProps">
        </template>
    </Timeline>
    </section>
</template>

<style scoped>

section {
    width: 100%;
    height: 500px;
    background-image: url('../assets/space.jpg');
    background: linear-gradient(circle, rgba(99, 97, 97, 0.63), rgba(0, 0, 0, 0.5)),
    url('../assets/space.jpg');
    background-repeat: no-repeat;
    background-size: cover;

    text-align: left;
    padding: 20px 200px;
    backdrop-filter: blur(10px)
}

.timeline {
    width: 100%;
    color:white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8)

}

p {
    display: block;
    text-align: center;
}

.timeline img {
    display: block;

    left: 0;
    transition: 300ms;
}

.premiere {
    color: #e50914d5;
}
.timeline img:hover{
    box-shadow: 2px 2px 61px 0px rgba(245,239,239,0.75);
    -webkit-box-shadow: 2px 2px 61px 0px rgba(245,239,239,0.75);
    -moz-box-shadow: 2px 2px 61px 0px rgba(245,239,239,0.75);
    cursor:pointer;
    transform: translateY(-5px);

}

</style>
