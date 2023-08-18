library(tidyverse)


calculate_gen_ci(0.501813784764208,0.505882352941176)

comp_calc <- function(df, gen1_id = 1){

calculate_gen_ci <- function(gen1_af, gen_af){
    ci <- log10(
        (gen1_af/gen_af - gen1_af)/( 1 - gen1_af)
        )
    return(ci)
}

#Calculates eq1 from Zhao for a strain, conditon, and replicate
    gen1_af <- df %>%
        filter(generation == gen1_id) %>%
        .$allele_freq 

    generations <- c(1,3,5,7)
    #create a blank vector to store the ci values
    cis <- c()
    #print(cis)
    #print("starting loop")
    for(generation_id in generations){
        #print(generation_id)
        gen_af <- df %>%
            filter(generation == generation_id) %>%
            .$allele_freq
        #print(gen_af)
        #print(gen_af)    
        ci <- calculate_gen_ci(gen1_af, gen_af)
        #print(ci)
        #print(ci)
        #add the ci to list of cis
        cis <- c(cis, ci)
        
    }
    return(cis)
}

#Test the function

test_strain_df <- comp_df %>%
    filter(strain == "N2")%>%
    filter(conditon == "DMSO")%>%
    filter(replicate == 1)

out <- comp_calc(test_strain_df, gen1_id = 1)
out
ci_lss <- function(ci_values){
    #takes a list of ci eq2 values and calculates ci 3 values
    # NOT SURE IF THE XS VALUES WILL ALWAYS BE TRUE
    xs <- c(0,2,4,6)
    xs_m <- as.matrix(xs) 
    reg <- lm.fit(xs_m, ci_values)
    val <- as.numeric(coef(reg))
    return(val) 
}

lm_data <- ci_lss(test_values)



cal_fitness <- function(lm_coef) {
    fitness <- log2(
        1 / 10^lm_coef
    )
    return(as.numeric(fitness))
}

cal_fitness(lm_data)

#Read-in the competiton data 
#a csv file with 5 columns 
#1. Strain
#2. Condition (Drug or No Drug)
#3. Generation
#4. Replicate
#5. Allele Frequency
comp_df <- data.table::fread("test_fitness.csv")




#Group the dataframe by strain, Generation, and replicate
#nest but keep the strain, generation, and replicate as columns
#Calculate the ci values for each strain, generation, and replicate
#then use the ci_values to calculate LSS and fitness

grouped <- comp_df %>%
    group_nest(strain, conditon, replicate, keep = TRUE) %>%
    mutate(ci_values = map(data, comp_calc, gen1_id = 1))%>%
    mutate(lm_coef = map_dbl(ci_values, ci_lss))%>%
    mutate(fitness = map_dbl(lm_coef, cal_fitness))

grouped$data
    


