#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <cstdio>
#include <iomanip>
#include <cmath>

#define USEDEBUG
#define VERBOSEDEBUG

#ifdef USEDEBUG
#define DEBUG_PRINT(x) std::cout << std::setprecision(2) << x << std::endl
#else
#define DEBUG_PRINT(x) 
#endif 

#ifdef VERBOSEDEBUG
#define VERBOSE_PRINT(x) std::cout << std::setprecision(2) << x << std::endl
#else
#define VERBOSE_PRINT(x) 
#endif 

uint32_t finCount = 0;
uint8_t sentDone = 0;
uint8_t nodesDone = 0;

const uint32_t nodeCount = {{ constants['totalNodeCount'] }};
const uint32_t tileCount = {{ constants['tileCount'] }};
uint32_t loopMax = 1000;

uint8_t fin[nodeCount];
uint16_t finIdx[nodeCount];
float avgHops[nodeCount];
uint32_t loopCount = 0;
