#ifndef VEC3_H
#define VEC3_H
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

std::vector<float> generateRandomPoint(float Radius, std::vector<float> pos, int num){
    std::vector<float> Random_Points;
    srand(time(0));
    for (int i = 1; i<=num; i++){
        int temp_num = (rand()%num);
    }
    return Random_Points;
};

int main(){
    int width = 256;
    int height = 256;
    std::ofstream out("my_image.ppm", std::ios::binary);
    out << "P6\n"<<width<<" "<<height<<"\n255\n";
    int progress = 0; // in percentage 
    for (int j = 0; j < height; j++){
        for (int i = 0; i<width; i++){
            unsigned char r = i;
            unsigned char g = j;
            unsigned char b = i+j;
            out.write(reinterpret_cast<char*>(&r), 1);
            out.write(reinterpret_cast<char*>(&g), 1);
            out.write(reinterpret_cast<char*>(&b), 1);            
        }
        std::cout<<"Task Completed : " << (j*100.0) / (height)<<std::endl;
    }
    out.close();
    std::cout<<"Task is Completed!"<<std::endl;
    return 0;
}
#endif