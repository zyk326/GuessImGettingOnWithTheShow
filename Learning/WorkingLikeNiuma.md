# This is AlphaFeature

## Format
(1)AlphaFeature.h + (2)AlphaFeatureImpl.h = AlphaFeature.cpp    
(1)里的是更新规则和一个总函数，它的cpp给函数体，函数体里给各种方法，这里的各种方法在(2)里面实现。  

## Detail
<1>  
C++设计上为了兼容通用指针，不让编译器自动推断出具体的类型。  
比如是void* m_p = nullptr;  
在使用时，必须自己强转成指定类型，来指定访问哪个具体类型。  
比如这样使用：((AlphaFeature*)m_p)->getSomeoneToMarry(image, name)      

<2>  
在析构函数里，对void* m_p进行释放的时候，需要强转指针类型再delete。  
使用比如：delete reinterpret_cast<AlphaFeatureImpl*>(m_p);    

<3>  
std::futrue<xxx>，这代表可以存放一个正在执行的异步任务的结果，存放的结果类型为<>指定的xxx类型。  

<4>  
使用异步处理的过程有多种写法，一个是直接使用函数指针，另一种使用lambda，两种写法不同，底层相同，建议用lambda，更优雅。  
```C++
成员函数指针的写法：  
for(int i = 0; i < modelresult.size(), i++){
    auto result = modelresult[i];  

    finalResult.push_back(
        std::async(
            std::launch::async,
            &AlphaFeatureImpl::getSub,
            ((AlphaFeatureImpl*)m_p),
            result
        );
    );
}  
```  
```c++
lambda的写法：  
for(int i = 0; i < modelresult.size(); i++){
    auto result = modelresult[i];

    auto* impl = reinterpret_cast<AlphaFeatureImpl*>(m_p);

    finalResult.push_back(
        std::async(
            std::launch::async, [impl, result](){
                return impl->getSub(result);
            }
        )
    )
}
```